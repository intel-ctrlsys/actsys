# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
from IPython.core.magic import (Magics, magics_class, line_magic)
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring, kwds)
from IPython.terminal.prompts import Prompts, Token
from .prompts import prompt, confirm


# The class MUST call this class decorator at creation time
@magics_class
class ShellCommands(Magics):
    system_default_root_device = {
        "hostname": "rocky",
        "location": "rocky",
        "device_type": "system"
    }
    system_default_config = {
        "device_types": {
            "system": {"abbreviation": "Sys", "required_fields": [], "optional_fields": [], "defaults": None},
            "rack": {"abbreviation": "R", "required_fields": [], "optional_fields": [], "defaults": None},
            "chassis": {"abbreviation": "CH", "required_fields": [], "optional_fields": [], "defaults": None},
            "node": {"abbreviation": "N", "required_fields": ["mac_address", "port"], "optional_fields": [], "defaults": None},
            "bmc": {"abbreviation": "B", "required_fields": ["mac_address", "access_type"], "optional_fields": [], "defaults": None},
            "pdu": {"abbreviation": "PD", "required_fields": [], "optional_fields": [], "defaults": None},
            "psu": {"abbreviation": "PS", "required_fields": [], "optional_fields": [], "defaults": None},
            "switch": {"abbreviation": "S", "required_fields": [], "optional_fields": [], "defaults": None}
        }
    }

    def __init__(self, shell, datastore):
        # Constructor for UserMagics class. Get the instance of ASD class
        super(ShellCommands, self).__init__()
        self.datastore = datastore
        self.device = None
        self.system_device = None
        self.system_config = None
        self.init_system_device()
        self.ipython = shell
        CustomPrompt(self.ipython, self.get_device_hierarchy(self.device))

    def init_system_device(self):
        self.device = self.datastore.get_device(self.system_default_root_device.get("hostname"))
        if self.device is None:
            self.datastore.set_device(self.system_default_root_device)
            self.device = self.datastore.get_device(self.system_default_root_device.get("hostname"))

        assert self.device is not None
        self.system_device = self.device

        config = self.datastore.get_configuration_value("cmm")
        if config is None:
            print("No configuration found for CMM, adding default configuration.")
            self.datastore.set_configuration("cmm", self.system_default_config)
            config = self.datastore.get_configuration_value("cmm")
        assert config is not None

        self.system_config = config

    @line_magic
    @magic_arguments()
    @argument('device', help='A list of devices. i.e node1, node[1-10], node3,node5.', nargs='?')
    def view(self, args):
        if args:
            device_str = parse_argstring(self.view, args).device
            device = self.datastore.get_device(device_str)
            if device:
                self.device = device
                CustomPrompt(self.ipython, self.get_device_hierarchy(device))
                print(("Switched view to {}".format(device_str)))
            else:
                print(("Could not view unknown device '{}'".format(device_str)))
                return

        device_name = self.device.get("hostname")
        location = self.device.get("location")

        print(("Viewing {} at location {}".format(device_name, location)))
        table_format = "\t{:<20}{:<20}{:<20}{!s:<20}"
        print((table_format.format("Name", "Type", "Location", "Children")))
        print("--------------------------------------------")
        children = self.get_device_children(device_name)
        for child in children:
            child_name = child.get("hostname")
            children_names = self.get_device_children(child_name)
            children_names = [x.get("hostname") for x in children_names]

            print((table_format.format(child_name, child.get("device_type"), child.get("location"), children_names)))

        print("")
        print(("{} configuration".format(device_name)))

        for f in self.device:
            key = (f[:18] + '..') if len(f) > 20 else f
            print(("\t{0:20} : {1}".format(key, self.device.get(f))))

        print("")
        self.print_help(device_name)

    @line_magic
    def add(self, args):
        """
        Every device requires: hostname, device_type, location
        Devices can require more depending on "required_fields"
        :param args:
        :return:
        """
        parent_name = self.device.get("hostname")
        device_type = prompt(message="What type of device would you like to add?",
                             choices=list(self.system_config.get("device_types").keys()))
        num_to_add = prompt("How many devices would you like to add?", validate=lambda _, x: x.isdigit())
        print("I would add '{}' devices, but I'm just a prototype, so adding 1.".format(num_to_add))
        name = self.generate_new_device_name(device_type)
        location = self.generate_new_device_location(self.device.get("location"), device_type)

        new_device = dict(parent=parent_name, device_type=device_type, hostname=name, location=location)

        # Set the required fields
        device_type_config = self._get_device_type_config(device_type)
        required_fields = device_type_config.get("required_fields")
        if required_fields:
            print("Please fill out the following required fields:")
        for rf in required_fields:
            ans = prompt("\t{}".format(rf))
            new_device[rf] = ans
        # Set the optional fields
        optional_fields = device_type_config.get("optional_fields")
        if optional_fields:
            print("Please fill out the following optional fields:")
        for of in optional_fields:
            ans = prompt("\t{}".format(of))
            new_device[of] = ans

        self.datastore.set_device(new_device)
        print(("Added device: {}".format(new_device)))

    @line_magic
    @magic_arguments()
    @argument('--devices', '-d', help='A list of devices. i.e node1, node[1-10], node3,node5.')
    def delete(self, args):
        """
        Attempts to delete any device name passed in, returning success if the device was deleted or already non-existant
        :param device_list: A list of devices. i.e node1, node[1-10], node3,node5.
        :return:
        """
        device_str = parse_argstring(self.delete, args).devices
        device_list = self.datastore.expand_device_list(device_str)

        if not device_list:
            # No device given to delete, so assuming its the current device
            device_str = self.device.get("hostname")
            device_list.append(device_str)

        children = self.get_device_children(device_list)
        if children:
            print("Can't delete {} because of children. Move the children to another parent first.")
            return

        delete_them = confirm("Are you sure you want to delete {}?".format(device_str))

        if delete_them:
            deleted_ids = self.datastore.delete_device(device_list)
            if deleted_ids:
                print(("Attempted to delete {} and removed the following ids: {}".format(device_str, deleted_ids)))
                if self.device.get("device_id") in deleted_ids:
                    self.view("rocky")
            else:
                print(("Nothing matching {} found to delete. Did you get the name right?".format(args)))

        print(("You can delete multiple devices by entering: delete -d {}".format(device_str)))

    @line_magic
    @magic_arguments()
    @argument('--devices', '-d', type=str, help='A list of devices. i.e node1, node[1-10], node3,node5.')
    @argument('--parent', '-p', type=str, help='A new parent device.')
    def move(self, args):
        parsed_args = parse_argstring(self.move, args)
        print(parsed_args)
        device_str = parsed_args.devices
        new_parent_device = parsed_args.parent
        device_list = self.datastore.expand_device_list(device_str)
        current_device_name = self.device.get("hostname")

        if not device_list:
            # Didn't give a device to move, so assume its the current selected device.
            device_list.append(current_device_name)

        if not new_parent_device:
            device_names = self.get_device_names()
            device_names.remove(current_device_name)
            prompt("Where would you like to move '{}' to?".format(current_device_name), choices=device_names)

        print(("Moving device(s) {} to new parent {}".format(device_str, new_parent_device)))
        print("Move not yet implemented")

        print(("Next time skip the prompts by entering: move -d {} -p {}".format(device_str, new_parent_device)))

    @line_magic
    def configure(self, args):
        configs = self.datastore.list_configuration()
        config_names = [x.get("key") for x in configs]
        result = prompt("Which configuration would you like to see?", choices=config_names)

        config = self.datastore.get_configuration_value(result)
        self.print_dict(config)

    @staticmethod
    def print_dict(printable, indent=''):
        """

        :param printable:
        :return:
        """

        if not isinstance(printable, dict):
            raise ValueError("print_dict only takes dict types")

        for key, value in list(printable.items()):
            key = (key[:18] + '..') if len(key) > 20 else key
            if isinstance(value, dict):
                print(("{0}{1:20}:".format(indent, key)))
                ShellCommands.print_dict(value, indent + '  ')
            else:
                print(("{0}{1:20}: {2}".format(indent, key, value)))

    def generate_new_device_name(self, device_type):
        """
        Devices are named like: <device_type><number>.
        :param device_type:
        :return:
        """
        num_devices_of_type = len(self.datastore.list_devices({"device_type": device_type}))
        return "{}{}".format(device_type, num_devices_of_type + 1)

    def _get_device_type_config(self, device_type):
        return self.system_config.get("device_types").get(device_type)

    def generate_new_device_location(self, parent_location, device_type):
        parent_children = self.get_device_children(parent_location)
        num_children = len([x for x in parent_children if x.get("device_type") == device_type])
        device_abbreviation = self._get_device_type_config(device_type).get("abbreviation")
        return "{}-{}{}".format(parent_location, device_abbreviation, num_children + 1)

    @staticmethod
    def print_help(device_name):
        print("(view) View {} again".format(device_name))
        print("(add) Add a new device to {}".format(device_name))
        print("(delete) Delete a device from {}".format(device_name))
        print("(move) Move a device from {} to another location".format(device_name))
        print("(copy) Copy {} to another location".format(device_name))
        print("(manage) Manage {}'s configuration".format(device_name))
        print("(configure) Manage software and CMM configuration.")
        print("(export <file_location>) Export the current configuration to a file.")
        print("(import <file_location>) Import a configuration from a file")
        print("(view <device>) view another device")

    def get_device_hierarchy(self, device):
        return device.get("hostname")

    def get_device_children(self, device_name):
        if isinstance(device_name, str) or isinstance(device_name, str):
            return self.datastore.list_devices({"parent": device_name})
        elif isinstance(device_name, list):
            children = []
            for device in device_name:
                children.extend(self.datastore.list_devices({"parent": device}))
            return children
        else:
            raise TypeError("Type {} not supported in func get_device_children".format(type(device_name)))

    def get_device_names(self):
        devices = self.datastore.list_devices()
        device_names = [x.get("hostname") for x in devices]
        return device_names


class CustomPrompt(Prompts):
    def __init__(self, ipython, cli_text):
        self.cli_text = cli_text
        super(CustomPrompt, self).__init__(ipython)
        ipython.prompts = self

    def in_prompt_tokens(self, cli=None):
        return [(Token.Prompt, self.cli_text + ' ['),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, ']: ')]
