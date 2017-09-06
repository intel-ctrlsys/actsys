# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
For handling the DataStore inteerface in postgres
"""

import json
import copy
import logging
import datetime
import psycopg2
from ClusterShell.NodeSet import NodeSet, RESOLVER_NOGROUP
from .datastore import DataStore, DataStoreException
from .utilities import DataStoreUtilities


class PostgresLogHandler(logging.Handler):
    """
    Log handler for prints log statments to the database.
    """

    def __init__(self, datastore):
        super(PostgresLogHandler, self).__init__()
        self.datastore = datastore

    def emit(self, record):
        try:
            self.datastore.add_log(record.levelno, record.msg, getattr(record, "device_name", None), record.name)
        except psycopg2.InterfaceError:
            self.datastore.connect()
            self.datastore.add_log(record.levelno, record.msg, getattr(record, "device_name", None), record.name)


class PostgresStore(DataStore):
    """
    Data Store interface.
    """

    def __init__(self, location, log_level=None):
        """
        Creates the object with parameters passed in. Then calles the connect method, and sets up
        the logger for use.
        :param location:
        :param log_level:
        """
        super(PostgresStore, self).__init__()
        self.connection_uri = location
        self.connection = None
        self.cursor = None
        self.connect()
        self.log_level = log_level if log_level is not None else DataStore.LOG_LEVEL
        self._setup_postgres_logger(log_level)

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()

    def _setup_postgres_logger(self, log_level):
        if log_level is None:
            log_level = DataStore.LOG_LEVEL

        postgres_handler = None
        for handler in self.logger.handlers:
            if isinstance(handler, PostgresLogHandler):
                postgres_handler = handler
                break

        if postgres_handler is None:
            postgres_handler = PostgresLogHandler(self)
            postgres_handler.setLevel(log_level)
            self.logger.addHandler(postgres_handler)
        else:
            postgres_handler.setLevel(log_level)

    def connect(self):
        """
        Close any open connections, and make them again. This will destroy any uncommited changes.

        :return:
        """
        if getattr(self, "cursor", None) is not None:
            self.cursor.close()
            self.connection.close()

        self.connection = psycopg2.connect(self.connection_uri)
        if self.connection is None:
            raise DataStoreException("Unable to connect to postgres with connection: `{}`".format(self.connection_uri))
        self.cursor = self.connection.cursor()

    def get_device(self, device_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).get_device(device_name)
        self.cursor.callproc("public.get_device_details", [str(device_name)])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.get_device database result: {}".format(result))
        devices = SqlParser.get_device_from_results(result)
        device = None
        if len(devices) >= 1:
            device = devices[0]
        self.logger.info("DataStore.get_device: {}".format(device))
        return device

    def list_devices(self, filters=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).list_devices(filters)
        self.cursor.callproc("public.get_device_details", [None])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.list_devices database result: {}".format(result))
        devices = SqlParser.get_device_from_results(result)
        filtered_devices = DataStoreUtilities.filter_dict(devices, filters)
        self.logger.info("DataStore.list_devices: {}".format(filtered_devices))
        return filtered_devices

    def set_device(self, device_info_list):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).set_device(device_info_list)

        if not isinstance(device_info_list, list):
            device_info_list = [device_info_list]

        set_ids = list()
        # TODO: change this for loop into one batch upsert query.
        for device_info in device_info_list:
            args = SqlParser.prepare_device_for_query(self._remove_profile_from_device(device_info)[0])
            self.cursor.callproc("public.upsert_device", args)
            result = self.cursor.fetchall()
            self.logger.debug("DataStore.set_device database result: {}".format(result))
            if result is None or len(result) != 1 or result[0][0] != 1:
                raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
            set_ids.append(result[0][1])

        self.connection.commit()
        return set_ids

    def delete_device(self, device_list):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).delete_device(device_list)
        if not isinstance(device_list, list):
            device_list = [device_list]

        deleted_device_ids = list()

        for device_name in device_list:
            device_name = str(device_name)
            self.cursor.callproc("public.delete_device", [device_name])
            result = self.cursor.fetchall()
            self.logger.debug("DataStore.delete_device database result: {}".format(result))
            if result is None or result[0][0] > 1:
                raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
            if result[0][0] == 1:
                # The affected device_id
                self.logger.debug("DataStore.delete_device deleted device: {}".format(result[0][1]))
                deleted_device_ids.append(result[0][1])
        self.connection.commit()

        return deleted_device_ids

    def get_device_history(self, device_name=None):
        super(PostgresStore, self).list_devices(device_name)
        args = list()
        if device_name is None:
            args.append(None)
        else:
            args.append(str(device_name))
        self.cursor.callproc("public.get_device_history", args)
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.get_device_history database result: {}".format(result))
        devices = SqlParser.get_device_from_results(result)
        self.logger.info("DataStore.get_device_history: {}".format(devices))
        return devices

    def get_profile(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).get_profile(profile_name)
        self.cursor.callproc("public.get_profile", [str(profile_name)])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.get_profile database result: {}".format(result))
        profiles = SqlParser.get_profile_from_results(result)
        profile = None
        if len(profiles) >= 1:
            profile = profiles[0]
        self.logger.info("DataStore.get_profile: {}".format(profile))
        return profile

    def list_profiles(self, filters=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).list_profiles(filters)
        self.cursor.callproc("public.get_profile", [None])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.list_profiles database result: {}".format(result))
        profiles = SqlParser.get_profile_from_results(result)
        filtered_profiles = DataStoreUtilities.filter_dict(profiles, filters)
        self.logger.info("DataStore.list_profiles: {}".format(filtered_profiles))
        return filtered_profiles

    def set_profile(self, profile_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).set_profile(profile_info)
        profile_name = profile_info.get("profile_name")
        args = SqlParser.prepare_profile_for_query(profile_info)
        self.cursor.callproc("public.upsert_profile", args)
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.set_profile database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if int(result[0][0]) == 1:
            self.logger.info("DataStore.set_profile affected profile: {}".format(profile_name))
            return profile_name
        else:
            self.logger.info("DataStore.set_profile affected profile: {}".format(None))
            return None

    def delete_profile(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).delete_profile(profile_name)
        self.cursor.callproc("public.delete_profile", [profile_name])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.delete_profile database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            self.logger.info("DataStore.delete_profile affected profile: {}".format(profile_name))
            return profile_name
        else:
            self.logger.info("DataStore.set_profile affected profile: {}".format(None))
            return None

    def list_logs(self, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).list_logs(device_name, limit)
        self.cursor.callproc("public.get_log", [device_name, limit])
        result = self.cursor.fetchall()
        result = SqlParser.get_log_from_results(result)
        self.logger.debug("DataStore.list_logs: Returned {} rows".format(len(result)))
        return result

    def list_logs_between_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).list_logs_between_timeslice(begin, end, device_name, limit)
        self.cursor.callproc("public.get_log_timeslice", [device_name, limit, begin, end])
        result = self.cursor.fetchall()
        result = SqlParser.get_log_from_results(result)
        self.logger.info("DataStore.list_logs_between_timeslice: Returned {} rows".format(len(result)))
        return result

    def add_log(self, level, msg, device_name=None, process=None):
        """
        See @DataStore for function description. Only implementation details here.

        No logging should happen inside this function... or it would be a recersive loop.
        """
        super(PostgresStore, self).add_log(level, msg, device_name, process)
        self.cursor.callproc("public.add_log",
                             [str(process), datetime.datetime.utcnow(), level, str(device_name), str(msg)])
        result = self.cursor.fetchall()
        if result is None or len(result) != 1 or result[0][0] != 1:
            raise DataStoreException("log add query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()

    def get_configuration_value(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).get_configuration_value(key)
        self.cursor.callproc("public.get_configuration_value", [key])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.get_configuration_value database result: {}".format(result))
        if result is not None and len(result) > 0:
            self.logger.info("DataStore.get_configuration_value: {}".format(result[0][0]))
            return result[0][0]
        else:
            self.logger.info("DataStore.get_configuration_value: None")
            return None

    def list_configuration(self):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).list_configuration()
        self.cursor.execute("SELECT key, value FROM public.configuration;")
        results = self.cursor.fetchall()
        return SqlParser.get_config_from_results(results)

    def set_configuration(self, key, value):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).set_configuration(key, value)
        self.cursor.callproc("public.upsert_configuration_value", [str(key), str(value)])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.set_configuration database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            self.logger.info("DataStore.delete_configuration updated key {}".format(key))
            return key
        else:
            self.logger.info("DataStore.delete_configuration updated key {}".format(None))
            return None

    def delete_configuration(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).delete_configuration(key)
        self.cursor.callproc("public.delete_configuration_value", [str(key)])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.delete_configuration database result: {}".format(result))
        if result is None or len(result) > 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            self.logger.info("DataStore.delete_configuration deleted key {}".format(key))
            return key
        else:
            self.logger.info("DataStore.delete_configuration deleted key {}".format(None))
            return None

    def list_groups(self):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).list_groups()
        self.cursor.execute("SELECT group_name, device_list FROM public.device_group;")
        results = self.cursor.fetchall()
        return SqlParser.get_groups_from_results(results)

    def get_group_devices(self, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).get_group_devices(group)
        self.cursor.execute("SELECT device_list FROM public.device_group WHERE group_name = %s;", [group])
        results = self.cursor.fetchall()
        if results and results[0]:
            return results[0][0]
        return None

    def add_to_group(self, device_list, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).add_to_group(device_list, group)
        group_devices = self.get_group_devices(group)

        updated_device_set = NodeSet(group_devices, resolver=RESOLVER_NOGROUP)
        device_list = super(PostgresStore, self).expand_device_list(device_list)
        updated_device_set.add(','.join(device_list))

        self.cursor.callproc("public.upsert_group", [group, str(updated_device_set)])
        result = self.cursor.fetchall()
        self.connection.commit()
        self.logger.debug("upsert_group result: {}".format(result))
        return updated_device_set

    def remove_from_group(self, device_list, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).remove_from_group(device_list, group)
        group_devices = self.get_group_devices(group)
        if group_devices is None:
            raise RuntimeError("Group {} doesn't exist".format(group))

        updated_device_set = NodeSet(group_devices, resolver=RESOLVER_NOGROUP)
        if device_list == '*':
            device_list = group_devices

        updated_device_set.remove(device_list)
        if len(updated_device_set) == 0:
            # Delete the group if its empty or user provided device_list is '*'
            self.cursor.execute("DELETE FROM public.device_group WHERE group_name = %s;", [group])
            updated_device_set = NodeSet()
        else:
            # Modify the group, because its not empty yet.
            self.cursor.callproc("public.upsert_group", [group, str(updated_device_set)])
            result = self.cursor.fetchall()
            self.logger.debug("upsert_group result: {}".format(result))

        self.connection.commit()
        return updated_device_set

    # CANNED QUERIES
    def get_devices_by_type(self, device_type, device_name=None):
        """
                See @DataStore for function description. Only implementation details here.
                """
        # super(PostgresStore, self).get_pdu()
        self.cursor.execute("SELECT * FROM public.get_device_details(%s) WHERE device_type = %s;",
                            [device_name, device_type])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.get_device_by_type database result: {}".format(result))
        return SqlParser.get_device_from_results(result)

    def export_to_file(self, file_location):
        """
        See @DataStore for function description. Only implementation details here.

        Exporting from the database to a file uses the filestore.
        """
        from .filestore import FileStore

        file = open(file_location, 'w')
        file.write('{ "configuration_variables": { "log_file_path": "' + file_location + '.log" } }')
        file.close()
        export_fs = FileStore(file_location, self.log_level)

        configuration = self.list_configuration()
        for config in configuration:
            export_fs.set_configuration(config["key"], config["value"])

        profiles = self.list_profiles()
        for profile in profiles:
            export_fs.set_profile(profile)

        devices = self.list_devices()
        for device in devices:
            # Removing device_history artifact
            device.pop("sys_period", None)
            export_fs.set_device(device)

        export_fs.save_file()

    def import_from_file(self, file_location):
        """
        See @DataStore for function description. Only implementation details here.

        Importing from a file uses the filestore to collect valid items.
        """
        from .filestore import FileStore

        # Check that we can parse and use this file for importing
        fs = FileStore(file_location, self.log_level)

        # Delete everything from current DB
        self.logger.info("Importing from file: Deleting old info")
        old_config, old_devices, old_profiles = self._delete_database()

        # import the new stuff
        try:
            self.logger.info("Importing from file: Importing File info")
            config_list = fs.list_configuration()
            for config in config_list:
                self.set_configuration(config["key"], config["value"])

            profiles = fs.list_profiles()
            for profile in profiles:
                self.set_profile(profile)

            devices = fs.list_devices()
            for device in devices:
                self.set_device(device)
        except Exception as ex:
            # Rollback any changes by closing the cursor / connection
            self.connect()
            # revert!
            self.logger.info("Importing from file: Reverting actions due to: {}".format(ex))
            self.logger.info("Importing from file: Clearing the database")
            self._delete_database()
            self.logger.info("Importing from file: Reverting config")
            for config in old_config:
                self.set_configuration(config["key"], config["value"])

            self.logger.info("Importing from file: Reverting profiles:")
            for profile in old_profiles:
                self.set_profile(profile)

            self.logger.info("Importing from file: Reverting devices:")
            for device in old_devices:
                self.set_device(device)

            # raise the exception that happened earlier
            raise

    def _delete_database(self):
        old_config = self.list_configuration()
        for config in old_config:
            self.delete_configuration(config["key"])

        old_devices = self.list_devices()
        for device in old_devices:
            self.delete_device(device["device_id"])

        old_profiles = self.list_profiles()
        for profile in old_profiles:
            self.delete_profile(profile["profile_name"])

        return old_config, old_devices, old_profiles


class SqlParser(object):
    """
    Helper class for converting SQL results to objects and objects to SQL params.
    """

    @staticmethod
    def get_device_from_results(results):
        """
        Parse results from SQL
        :param results:
        :return:
        """
        devices = list()
        for result in results:
            device = dict()
            device["device_id"] = result[0]
            device["device_type"] = result[1]
            # device["properties"] = result[2]
            if result[3] is not None:
                device["hostname"] = result[3]
            if result[4] is not None:
                device["ip_address"] = result[4]
            if result[5] is not None:
                device["mac_address"] = result[5]
            if result[6] is not None:
                device["profile_name"] = result[6]
            # device["profile_properties"] = result[7]
            if len(result) >= 9:
                device["sys_period"] = result[8]

            if result[2] is not None:
                for prop_key in result[2]:
                    if prop_key not in device:
                        device[prop_key] = result[2][prop_key]

            if result[7] is not None:
                for prop_key in result[7]:
                    if prop_key not in device:
                        device[prop_key] = result[7][prop_key]

            devices.append(device)
        return devices

    @staticmethod
    def get_profile_from_results(results):
        """
        Takes the list_profiles results and translates them into a profile object.
        :param results: the results from the psycop2 SQL query
        :return: A List of profile objects
        """
        profiles = list()
        for result in results:
            profile = dict()
            profile["profile_name"] = result[0]
            properties = result[1]

            if properties is not None:
                for prop_key in properties:
                    profile[prop_key] = properties[prop_key]

            profiles.append(profile)

        return profiles

    @staticmethod
    def get_log_from_results(results):
        """

        :param results:
        :return:
        """
        logs = list()
        for result in results:
            logs.append({
                "process": result[0],
                "timestamp": result[1],
                "level": result[2],
                "device_id": result[3],
                "message": result[4]
            })

        return logs

    @staticmethod
    def get_config_from_results(results):
        """

        :param results:
        :return:
        """
        configuration_list = list()
        for result in results:
            configuration_list.append({
                "key": result[0],
                "value": result[1]
            })

        return configuration_list

    @staticmethod
    def get_groups_from_results(results):
        """

        :param results:
        :return:
        """
        groups = dict()
        for result in results:
            groups[result[0]] = result[1]

        return groups

    @staticmethod
    def prepare_profile_for_query(profile):
        """
        Takes a dict or object and creates the appropriate arguments (profile_name, properties) for
        inserting this into the database.
        :param profile: An object or dict with key/attributes to turn into JSON. The only special
            attribute in this action is the 'profile_name' which is extracted and put as the first
            object in the returned array.
        :return: [profile_name:string, properties:json_string]
        """
        # Handle a dict
        profile = copy.deepcopy(profile)
        if not isinstance(profile, dict):
            raise RuntimeError("Cannot prepare profile of unknown type for query, please pass a dict.")

        profile_name = profile.pop('profile_name', None)
        return [profile_name, json.dumps(profile)]

    @staticmethod
    def prepare_device_for_query(device):
        """
        Takes a dict or object and creates the appropriate arguments (profile_name, properties) for
        inserting this into the database.
        :param device: An object or dict with key/attributes to turn into JSON. The only special
            attribute in this action is the 'profile_name' which is extracted and put as the first
            object in the returned array.
        :return: [profile_name:string, properties:json_string]
        """

        def pop_to_string(dvc, param):
            """Converts whats given to a string or None"""
            temp = dvc.pop(param, None)
            if temp is not None:
                temp = str(temp)
            return temp

        # Handle a dict
        device = copy.deepcopy(device)
        if not isinstance(device, dict):
            raise RuntimeError("Cannot prepare device of unknown type for query, please pass a dict.")
        device_id = pop_to_string(device, 'device_id')
        device_type = pop_to_string(device, "device_type")
        hostname = pop_to_string(device, "hostname")
        ip_address = pop_to_string(device, "ip_address")
        mac_address = pop_to_string(device, "mac_address")
        hardware_type = pop_to_string(device, "hardware_type")
        profile_name = pop_to_string(device, "profile_name")
        device.pop("sys_period", None)
        return [device_id, device_type, hostname, ip_address, mac_address, hardware_type, profile_name,
                json.dumps(device)]
