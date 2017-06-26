# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright (c) 2017 Intel Corp.
#
"""
This module creates the command line parser and executes the user commands.
"""
from __future__ import print_function
import argparse
import re
from dateutil.parser import parse as date_parse
from . import DataStoreException, DataStore, DataStoreBuilder
from .utilities import DeviceUtilities, FileNotFound, NonParsableFile


class DataStoreCLI(object):
    """
    DataStore Command Line Interface
    """

    def __init__(self, datastore):
        self.root_parser = argparse.ArgumentParser(prog='datastore')
        self.retval = 0
        # Check for or create a DataStore
        if isinstance(datastore, DataStore):
            self.datastore = datastore
        elif isinstance(datastore, str):
            self.datastore = DataStoreBuilder.get_datastore_from_string(datastore)
        else:
            raise ValueError("Cannot construct a datastore object with passed in `{}`".format(datastore))

        self.subparsers = self.root_parser.add_subparsers(title='Data Type', description='What datatype to manipulate')
        self.add_device_args()
        self.add_profile_args()
        self.add_config_args()
        self.add_log_args()
        self.add_export_args()
        self.add_import_args()
        self.add_group_args()

    def add_device_args(self):
        """
        Add arguments for device manipulations
        :return:
        """
        self.device_parser = self.subparsers.add_parser('device', help="Manipulations for devices")
        self.device_parser.add_argument('action', choices=['list', 'get', 'set', 'delete'])
        self.device_parser.add_argument('device_list', nargs='?', default=None)
        self.device_parser.add_argument('options', nargs='*',
                                        help='key=value pairs used to assist in selecting and setting attributes')
        self.device_parser.set_defaults(func=self.device_execute)

    def add_profile_args(self):
        """
        Add arguments for profile manipulations
        :return:
        """
        self.profile_parser = self.subparsers.add_parser('profile', help="Manipulations for profiles")
        self.profile_parser.add_argument('action', choices=['list', 'get', 'set', 'delete'])
        self.profile_parser.add_argument('profile_name', nargs='?', default=None)
        self.profile_parser.add_argument('options', nargs='*',
                                         help='key=value pairs used to assist in selecting and setting attributes')
        self.profile_parser.set_defaults(func=self.profile_execute)

    def add_config_args(self):
        """
        Add arguments for configuration manipulations
        :return:
        """
        self.config_parser = self.subparsers.add_parser('config', help="Manipulations for configuration")
        self.config_parser.add_argument('action', choices=['list', 'get', 'set', 'delete'])
        self.config_parser.add_argument('key', nargs='?', default=None)
        self.config_parser.add_argument('value', nargs='?', default=None)
        self.config_parser.set_defaults(func=self.config_execute)

    def add_log_args(self):
        """
        Add arguments for log manipulations
        :return:
        """
        self.log_parser = self.subparsers.add_parser('log', help="Manipulations for logs",
                                                     formatter_class=argparse.RawTextHelpFormatter)
        self.log_parser.add_argument('action', choices=['list', 'get'])
        # To get multiline help msgs:
        # http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text
        self.log_parser.add_argument('--limit', '-l', type=int, default=100, required=False)
        self.log_parser.add_argument('--device_list', '-n', type=str, required=False)
        self.log_parser.add_argument('--begin', '-b', required=False)
        self.log_parser.add_argument('--end', '-e', required=False)

        # self.log_parser.add_argument('options', nargs='*', help='''key=value pairs used to assist in selecting
        # and setting attributes
        # More
        # ... and more
        # ...and more!''')
        self.log_parser.set_defaults(func=self.log_execute)

    def add_import_args(self):
        """
        Add arguments for importing a DataStore configuration. This will delete any current DataStore configuration.
        :return:
        """
        self.import_parser = self.subparsers.add_parser('import', help="Import a configuration into the datastore, "
                                                                       "overwriting the current information.",
                                                        description="Import from a valid configuration file. A valid"
                                                                    " import includes devices, profiles and"
                                                                    " configuration values. This command deletes"
                                                                    " existing data, so be sure to export your current"
                                                                    " configuration first if you want to save it.")
        self.import_parser.add_argument('file_location', help="The file location to be used for the import.")
        self.import_parser.set_defaults(func=self.import_execute)

    def add_export_args(self):
        """
        Add arguments for exporting the current configuration of the DataStore.
        :return:
        """
        self.export_parser = self.subparsers.add_parser('export', help="Export a configuration from the datastore, "
                                                                       "to a file.",
                                                        description="Export the current config to a file location. This"
                                                                    " export includes devices, profiles, and"
                                                                    " configuration values. It does not include device"
                                                                    " history or logs.")
        self.export_parser.add_argument('file_location', help="where to export this configuration too.")
        self.export_parser.set_defaults(func=self.export_execute)

    def add_group_args(self):
        """
        Add arguments for adding, removing and listing groups. Usage is something like:
        $ group list
        @all c[1-10]
        $ ...group add c[1-10] test
        Success.
        $ group remove c[6-10] test
        Sucess.
        $ group list
        @all c[1-10]
        @test c[1-5]
        $
        :return:
        """
        group_parser = self.subparsers.add_parser('group', help="Add/Remove devices to/from groups. List known "
                                                                "groups.",
                                                  description="Handle grouping for ease in using ctrl. Groups"
                                                              " manipulated in this way are stored and handled"
                                                              " via the DataStore. Groups can also be maintained"
                                                              " manually via ClusterShell. See the ClusterShell"
                                                              " documentation for advanced group configurations.")
        group_subparsers = group_parser.add_subparsers(help='subparser for group')
        self._add_add_parser(group_subparsers)
        self._add_remove_parser(group_subparsers)
        self._add_get_parser(group_subparsers)
        self._add_list_parser(group_subparsers)
        self._add_expand_parser(group_subparsers)
        self._add_fold_parser(group_subparsers)
        self._add_groups_parser(group_subparsers)

        group_parser.add_argument('--datastore-only', '-d', type=bool, default=False, required=False,
                                  help="Only use the datastore when retrieving groups, ignore any other"
                                       " ClusterShell set groups (i.e. SLURM or Genders groups).")

    def _add_add_parser(self, group_parser):
        add_parser = group_parser.add_parser('add', help='Add device regex to group. Use: group add '
                                                         'node_regex group_name')
        add_parser.add_argument('device_list', help='provide comma separated device list or device regex')
        add_parser.add_argument('group', help='group name where the devices have to be added to')
        add_parser.set_defaults(func=self.group_add_execute)

    def _add_remove_parser(self, group_parser):
        remove_parser = group_parser.add_parser('remove', help='Remove device regex from group. Use: group'
                                                               ' remove node_regex group_name')
        remove_parser.add_argument('device_list', help='provide comma separated device list or device regex')
        remove_parser.add_argument('group', help='group name where the devices have to be added to')
        remove_parser.set_defaults(func=self.group_remove_execute)

    def _add_get_parser(self, group_parser):
        get_parser = group_parser.add_parser('get', help='Get the device regex from group. Use: group get group_name')
        get_parser.add_argument('group', help='group name where the devices have to be added to')
        get_parser.set_defaults(func=self.group_get_execute)

    def _add_list_parser(self, group_parser):
        list_parser = group_parser.add_parser('list', help='list the groups created so far. Use: group list')
        list_parser.set_defaults(func=self.group_list_execute)

    def _add_expand_parser(self, group_parser):
        expand_parser = group_parser.add_parser('expand', help='expand the device regex or/and group into list of '
                                                               'devices. Use: group expand group_name,device_regex')
        expand_parser.add_argument('device_list', help='provide comma separated device list or device regex or group '
                                                       'name')
        expand_parser.set_defaults(func=self.group_expand_execute)

    def _add_fold_parser(self, group_parser):
        fold_parser = group_parser.add_parser('fold', help='fold the device list into device regex Use: group fold'
                                                           ' device_list')
        fold_parser.add_argument('device_list', help='provide comma separated device list or device regex')
        fold_parser.set_defaults(func=self.group_fold_execute)

    def _add_groups_parser(self, group_parser):
        groups_parser = group_parser.add_parser('groups', help='list the groups where the device regex is available. '
                                                               'Use: group groups device_regex')
        groups_parser.add_argument('device_list', help='provide comma separated device list or device regex')
        groups_parser.set_defaults(func=self.group_groups_execute)


    def parse_and_run(self, args=None):
        """
        Parse the args passed in or from sys.argv and run the function they indicate.
        :param args:
        :return:
        """
        if args is None:
            args = self.root_parser.parse_args()
        else:
            args = self.root_parser.parse_args(args)
        try:
            self.retval = args.func(args)
        except (DataStoreException, DataStore.DeviceListParseError) as dse:
            self.root_parser.print_usage()
            print(dse)
            return 1
        return self.retval

    def device_execute(self, parsed_args):
        """

        :param parsed_args:
        :return:
        """
        device_list = parsed_args.device_list

        try:
            options = self.parse_options(parsed_args.options)
        except ParseOptionsException as poe:
            print(poe.message)
            return poe.return_code

        if parsed_args.action == "list":
            new_options = options.copy()
            if device_list is not None:
                try:
                    ops2 = self.parse_options([device_list])
                except ParseOptionsException as poe:
                    print(poe.message)
                    return poe.return_code
                new_options.update(ops2)
            devices = self.datastore.list_devices(new_options)
            self.print_devices(devices)
            return 0

        device_list = DeviceUtilities.expand_devicelist(device_list)
        if not device_list:
            self.device_parser.print_usage()
            print("Please specify a device")
            return 1

        if parsed_args.action == "set":
            devices_to_be_set = list()
            for device_name in device_list:
                # TODO: turn this get into one call to get all the devices (maybe use list_device(hostnames)?)
                existing_device = self.datastore.get_device(device_name)
                if existing_device is None:
                    existing_device = dict()

                # TODO: put this in a datastore function, (called update device, instead of set)
                # Apply the options to it
                for option in options:
                    value = options[option]
                    if value == "UNDEF":
                        existing_device.pop(option, None)
                    else:
                        existing_device[option] = value

                if existing_device.get("device_type") is None:
                    self.device_parser.print_usage()
                    print("Please specify a device_type. (i.e device_type=node) for device {}".format(device_name))
                    return 1

                # Set profile_name in the options
                existing_device["hostname"] = existing_device.get("hostname", device_name)

                devices_to_be_set.append(existing_device)

            self.datastore.set_device(devices_to_be_set)
            print("Successfully updated '{}'".format(device_list))

            return 0

        if parsed_args.options:
            self.device_parser.print_usage()
            print("device {} does not accept additional options.".format(parsed_args.action))
            return 1

        if parsed_args.action == "get":
            if len(device_list) > 1:
                print("'device get' only supports getting one device at a time. "
                      "The passed in device list contains {} devices.".format(len(device_list)))
                return 1
            device = self.datastore.get_device(device_list[0])
            if device is None:
                print("Could not find any device matching {}".format(device_list))
                return 1
            self.print_devices(device)
            return 0

        if parsed_args.action == "delete":
            retval = self.datastore.delete_device(device_list)
            if not retval:
                print("Device(s) not found. Nothing was deleted.")
            else:
                print("Successfully deleted {}".format(retval))
            return 0

    def profile_execute(self, parsed_args):
        """

        :param parsed_args:
        :return:
        """
        profile_name = parsed_args.profile_name
        try:
            options = self.parse_options(parsed_args.options)
        except ParseOptionsException as poe:
            print(poe.message)
            return poe.return_code

        if parsed_args.action == "list":
            # Copy profile_name to options, profile list doen not accept a profile_name
            new_options = options.copy()
            if profile_name is not None:
                try:
                    ops2 = self.parse_options([profile_name])
                except ParseOptionsException as poe:
                    print(poe.message)
                    return poe.return_code
                new_options.update(ops2)
            profiles = self.datastore.list_profiles(new_options)
            self.print_devices(profiles)
            return 0

        if profile_name is None:
            self.profile_parser.print_usage()
            print("Please specify a profile_name")
            return 1

        if parsed_args.action == "set":
            # Get an existing profile, we set all the passed in options in the profile and
            # delete the ones where value is UNDEF
            existing_profile = self.datastore.get_profile(profile_name)
            if existing_profile is None:
                existing_profile = dict()

            # Apply the options to it
            for option in options:
                value = options[option]
                if value == "UNDEF":
                    existing_profile.pop(option, None)
                else:
                    existing_profile[option] = value

            # Set profile_name in the options
            existing_profile["profile_name"] = existing_profile.get("profile_name", profile_name)
            self.datastore.set_profile(existing_profile)
            print("Profile '{}' updated".format(profile_name))
            return 0

        if parsed_args.options:
            self.profile_parser.print_usage()
            print("profile {} does not accept additional options.".format(parsed_args.action))
            return 1

        if parsed_args.action == "get":
            profile = self.datastore.get_profile(profile_name)
            if profile is None:
                print("Could not find any profile matching {}".format(profile_name))
                return 1
            self.print_devices(profile)
            return 0
        if parsed_args.action == "delete":
            retval = self.datastore.delete_profile(profile_name)
            if retval is None:
                print("Profile not found. Nothing was deleted.")
            else:
                print("Sucessfully deleted '{}'".format(retval))
            return 0

        self.profile_parser.print_usage()
        print("Please specify an action")
        return 1

    def config_execute(self, parsed_args):
        """

        :param parsed_args:
        :return:
        """
        if parsed_args.action == "list":
            config_list = self.datastore.list_configuration()
            for config in config_list:
                config_key = config.get("key")
                config_value = config.get("value")
                key = (config_key[:28] + '..') if len(config_key) > 28 else config_key
                print("{0:30} : {1}".format(key, config_value))
            return 0

        config_key = parsed_args.key
        if config_key is None:
            self.config_parser.print_usage()
            print("Please specify a key to retrieve from the config")
            return 1

        if parsed_args.action == "get":
            config_value = self.datastore.get_configuration_value(config_key)
            if config_value is None:
                print("Value for key `{}` not found".format(config_key))
                return 1
            print("{} : {}".format(config_key, config_value))
            return 0
        if parsed_args.action == "delete":
            self.datastore.delete_configuration(config_key)
            print("Deleted")
            return 0
        if parsed_args.action == "set":
            config_value = parsed_args.value
            if config_value is None:
                self.config_parser.print_usage()
                print("Please specify a value. (i.e. config foo bar)")
                return 1

            set_key = self.datastore.set_configuration(config_key, config_value)
            print("Successfully set {}, to {}".format(set_key, config_value))
            return 0

    def log_execute(self, parsed_args):
        """

        :param parsed_args:
        :return:
        """
        if parsed_args.begin is not None:
            print(parsed_args.begin)
            if parsed_args.end is None:
                self.log_parser.print_usage()
                print("If you specify a beginning time, you must specify an end time  as well.")
                return 0
            begin_date = date_parse(parsed_args.begin)
            end_date = date_parse(parsed_args.end)
            result = self.datastore.list_logs_between_timeslice(begin_date, end_date, parsed_args.device_list,
                                                                parsed_args.limit)
            self.print_devices(result)
            return 0
        else:
            result = self.datastore.list_logs(parsed_args.device_list, parsed_args.limit)
            self.print_devices(result)
            return 0

    def import_execute(self, parsed_args):
        """

        :param parsed_args:
        :return:
        """
        self.datastore.import_from_file(parsed_args.file_location)
        return 0

    def export_execute(self, parsed_args):
        """

        :param parsed_args:
        :return:
        """
        self.datastore.export_to_file(parsed_args.file_location)
        return 0

    def group_add_execute(self, parsed_args):
        """
        Add nodes to group
        :param parsed_args:
        :return:
        """
        device_list = parsed_args.device_list
        group = parsed_args.group
        try:
            result = self.datastore.add_to_group(device_list, group)
            print("Group {} has been updated to {}".format(group, result))
        except (FileNotFound, NonParsableFile) as ex:
            print(str(ex))
        return 0

    def group_remove_execute(self, parsed_args):
        """
        Remove nodes from group
        :param parsed_args:
        :return:
        """
        device_list = parsed_args.device_list
        group = parsed_args.group
        try:
            result = self.datastore.remove_from_group(device_list, group)
            print("Group {} has been updated to {}".format(group, result))
        except (FileNotFound, NonParsableFile) as ex:
            print(str(ex))
        return 0

    def group_get_execute(self, parsed_args):
        """
        show the nodes in group
        :param parsed_args:
        :return:
        """
        group = parsed_args.group
        devices = self.datastore.get_group_devices(group)
        print(devices)
        return 0

    def group_list_execute(self, parsed_args=None):
        """
        list the groups
        :param parsed_args:
        :return:
        """
        groups = self.datastore.list_groups()
        group_keys = sorted(groups.keys())
        for group in group_keys:
            print("{0}".format(group))
            # TODO: print out the devices too. This can't be done right now or it
            # will break the clustershell CLI. (i.e. nodeset -s datastore -L)
            # So an additional arg like --simple should be added to differenciate.
            # print("{0:10}: {1}".format(group, groups.get(group)))

        if not groups:
            print("No groups found.")
        return 0

    def group_expand_execute(self, parsed_args):
        """
        Expand the groups
        :param parsed_args:
        :return:
        """
        device_list = parsed_args.device_list
        print(self.datastore.expand_device_list(device_list))
        return 0

    def group_fold_execute(self, parsed_args):
        """
        Fold the group
        :param parsed_args:
        :return:
        """
        device_list = parsed_args.device_list
        print(self.datastore.fold_devices(device_list))
        return 0

    def group_groups_execute(self, parsed_args):
        """
        Show which groups the nodes belong to
        :param parsed_args:
        :return:
        """
        device_list = parsed_args.device_list

        # All groups a device belongs too
        device_groups = self.datastore.get_device_groups(device_list)
        if not device_groups:
            print("{} nodes are not part of same groups".format(device_list))
            return 0
        print("{} is a member of groups:".format(device_list))
        for group in device_groups:
            print("{}".format(group))
        return 0

    @staticmethod
    def parse_options(options):
        """

        :param options: A list like: ['foo=bar', 'baz=1', 'joe=[do,re,me]']
        :return:
        """
        options_dict = dict()
        if options is None:
            return options_dict
        for option in options:
            temp = option.split("=")

            # Accepts options like 'foo=bar'
            if len(temp) < 2:
                raise ParseOptionsException(1, "Option `{}` is not valid. Please specify a value like"
                                               " key=value.".format(option))
            elif len(temp) > 2:
                key = temp[0]
                value = "=".join(temp[1:])
            else:
                key = temp[0]
                value = temp[1]

            # None or empty str, is not allowed
            if key is None or key == '' or value is None or value == '':
                raise ParseOptionsException(1, "Option `{}` is not valid. Please specify a value like"
                                               " key=value.".format(option))

            # Check for lists
            # Test it is a list:
            if re.search(r"(^\[.*\]$)", value) is not None:
                # get the individual items in the list
                matches = re.findall(r"([^\[\],]+)", value)
                value = list()
                for match in matches:
                    match = match.strip()
                    if match is not None and match != '':
                        if match.isdigit():
                            match = int(match)
                        value.append(match)

            # Check for and parse digits
            if isinstance(key, str) and key.isdigit():
                key = int(key)
            if isinstance(value, str) and value.isdigit():
                value = int(value)

            # Check if the key already exists, we do not allow duplicate keys
            if options_dict.get(key):
                raise ParseOptionsException(1, "Key `{}` was found more than once. Please make sure your keys "
                                               "in the options list are unique.".format(key))

            # Set the option
            options_dict[key] = value

        return options_dict

    @staticmethod
    def print_devices(printable):
        """

        :param printable:
        :return:
        """
        if not isinstance(printable, list):
            printable = [printable]

        if len(printable) == 0:
            print("No item(s) found.")

        for item in printable:
            # Pass this list in, with the device types so that the output can be something like:
            # --- Device: compute-29 ---
            # or
            # --- Profile: compute_node ---
            # Header:
            device_list = item.get("hostname") or item.get("device_id") \
                          or item.get("ip_address") or item.get("profile_name")
            print("--- {} ---".format(device_list))

            # Body:
            if isinstance(item, dict):
                for f in item:
                    key = (f[:18] + '..') if len(f) > 20 else f
                    print("{0:20} : {1}".format(key, item.get(f)))


class ParseOptionsException(Exception):
    """
    A staple exception for when option parsing errors happen. Never exposed to the user, only used internally.
    """

    def __init__(self, return_code, msg):
        super(ParseOptionsException, self).__init__()
        self.return_code = return_code
        self.message = msg
