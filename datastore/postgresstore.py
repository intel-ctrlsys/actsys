# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
import psycopg2
import json
import copy
import logging
import datetime
from .datastore import DataStore, DataStoreException


class PostgresLogHandler(logging.Handler):
    def __init__(self, datastore):
        super(PostgresLogHandler, self).__init__()
        self.datastore = datastore

    def emit(self, record):
        try:
            self.datastore.log_add(record.levelno, record.msg, getattr(record, "device_name", None), record.name)
        except psycopg2.InterfaceError:
            self.datastore.connect()
            self.datastore.log_add(record.levelno, record.msg, getattr(record, "device_name", None), record.name)


class PostgresStore(DataStore):
    """
    Data Store interface.
    """

    def __init__(self, location, log_level):
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
        self._setup_postgres_logger(log_level)

    def __del__(self):
        self.cursor.close()
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
        self.cursor = self.connection.cursor()

    def device_get(self, device_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_get(device_name)
        args = list()
        if device_name is None:
            args.append(None)
        else:
            args.append(str(device_name))
        self.cursor.callproc("public.get_device_details", args)
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.device_get database result: {}".format(result))
        devices = SqlParser.get_device_from_results(result)
        self.logger.info("DataStore.device_get: {}".format(devices))
        return devices

    def device_upsert(self, device_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_upsert(device_info)

        args = SqlParser.prepare_device_for_query(self._remove_profile_from_device(device_info)[0])
        self.cursor.callproc("public.upsert_device", args)
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.device_upsert database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()

        if result[0][0] == 1:
            self.logger.info("DataStore.device_upsert affected device: {}".format(result[0][1]))
            # The affected device_id
            return result[0][1]
        else:
            # Nothing changed
            self.logger.info("DataStore.device_upsert affected device: None")
            return None

    def device_logical_delete(self, device_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_logical_delete(device_name)
        device_name = str(device_name)
        self.cursor.callproc("public.delete_device_logical", [device_name])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.device_logical_delete database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            # The affected device_id
            self.logger.info("DataStore.device_logical_delete deleted device: {}".format(result[0][1]))
            return result[0][1]
        else:
            # Nothing changed
            self.logger.info("DataStore.device_logical_delete deleted device: {}".format(None))
            return None

    def device_fatal_delete(self, device_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_fatal_delete(device_name)
        device_name = str(device_name)
        self.cursor.callproc("public.delete_device_fatal", [device_name])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.device_fatal_delete database result: {}".format(result))
        if result is None or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            # The affected device_id
            self.logger.info("DataStore.device_logical_fatal deleted device: {}".format(result[0][1]))
            return result[0][1]
        else:
            # Nothing changed
            self.logger.info("DataStore.device_logical_fatal deleted device: {}".format(None))
            return None

    def profile_get(self, profile_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).profile_get(profile_name)
        self.cursor.callproc("public.get_profile", [profile_name])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.profile_get database result: {}".format(result))
        profiles = SqlParser.get_profile_from_results(result)
        self.logger.info("DataStore.profile_get: {}".format(profiles))
        return profiles

    def profile_upsert(self, profile_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).profile_upsert(profile_info)
        profile_name = profile_info.get("profile_name")
        args = SqlParser.prepare_profile_for_query(profile_info)
        self.cursor.callproc("public.upsert_profile", args)
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.profile_upsert database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if int(result[0][0]) == 1:
            self.logger.info("DataStore.profile_upsert affected profile: {}".format(profile_name))
            return profile_name
        else:
            self.logger.info("DataStore.profile_upsert affected profile: {}".format(None))
            return None

    def profile_delete(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).profile_delete(profile_name)
        self.cursor.callproc("public.delete_profile", [profile_name])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.profile_delete database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            self.logger.info("DataStore.profile_delete affected profile: {}".format(profile_name))
            return profile_name
        else:
            self.logger.info("DataStore.profile_upsert affected profile: {}".format(None))
            return None

    def log_get(self, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).log_get(device_name, limit)
        self.cursor.callproc("public.get_log", [device_name, limit])
        result = self.cursor.fetchall()
        result = SqlParser.get_log_from_results(result)
        self.logger.debug("DataStore.log_get: Returned {} rows".format(len(result)))
        return result

    def log_get_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).log_get_timeslice(begin, end, device_name, limit)
        self.cursor.callproc("public.get_log_timeslice", [device_name, limit, begin, end])
        result = self.cursor.fetchall()
        result = SqlParser.get_log_from_results(result)
        self.logger.info("DataStore.log_get_timeslice: Returned {} rows".format(len(result)))
        return result

    def log_add(self, level, msg, device_name=None, process=None):
        """
        See @DataStore for function description. Only implementation details here.

        No logging should happen inside this function... or it would be a recersive loop.
        """
        super(PostgresStore, self).log_add(level, msg, device_name, process)
        self.cursor.callproc("public.add_log",
                             [str(process), datetime.datetime.utcnow(), level, str(device_name), str(msg)])
        result = self.cursor.fetchall()
        if result is None or len(result) != 1 or result[0][0] != 1:
            raise DataStoreException("log add query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()

    def configuration_get(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).configuration_get(key)
        self.cursor.callproc("public.get_configuration_value", [key])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.configuration_get database result: {}".format(result))
        if result is not None and len(result) > 0:
            self.logger.info("DataStore.configuration_get: ".format(result[0][0]))
            return result[0][0]
        else:
            self.logger.info("DataStore.configuration_get: ".format(None))
            return None

    def configuration_upsert(self, key, value):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).configuration_upsert(key, value)
        args = [str(key), str(value)]
        # Cant use callproc: http://stackoverflow.com/a/28410398/1767377
        self.cursor.callproc("public.upsert_configuration_value", [str(key), str(value)])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.configuration_upsert database result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            self.logger.info("DataStore.configuration_delete updated key {}".format(key))
            return key
        else:
            self.logger.info("DataStore.configuration_delete updated key {}".format(None))
            return None

    def configuration_delete(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).configuration_delete(key)
        self.cursor.callproc("public.delete_configuration_value", [str(key)])
        result = self.cursor.fetchall()
        self.logger.debug("DataStore.configuration_delete database result: {}".format(result))
        if result is None or len(result) > 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            self.logger.info("DataStore.configuration_delete deleted key {}".format(key))
            return key
        else:
            self.logger.info("DataStore.configuration_delete deleted key {}".format(None))
            return None

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


class SqlParser(object):
    """
    Helper class for converting SQL results to objects and objects to SQL params.
    """

    @staticmethod
    def get_device_from_results(results):
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
        Takes the profile_get results and translates them into a profile object.
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
        def pop_to_string(d, p):
            """Converts whats given to a string or None"""
            t = d.pop(p, None)
            if t is not None:
                t = str(t)
            return t

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
        return [device_id, device_type, hostname, ip_address, mac_address, hardware_type, profile_name,
                json.dumps(device)]
