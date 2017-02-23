# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
from .datastore import DataStore, DataStoreException
import psycopg2
import json
from .utilities import DataStoreUtilities
from uuid import uuid4
import copy


class PostgresStore(DataStore):
    """
    Data Store interface.
    """
    def __init__(self, print_to_screen, location):
        super(PostgresStore, self).__init__(print_to_screen)
        self.connection = psycopg2.connect(location)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def device_get(self, device_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_get(device_name)
        self.cursor.callproc("public.get_device_details", [str(device_name)])

        return SqlParser.get_device_from_results(self.cursor.fetchall())

    def device_upsert(self, device_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_upsert(device_info)
        # No upserting skus!
        device_info.pop("sku", None)

        args = SqlParser.prepare_device_for_query(self._remove_profile_from_device(device_info)[0])
        self.cursor.callproc("public.upsert_device", args)
        result = self.cursor.fetchall()
        self._print_if_ok("device_upsert result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()

        if result[0][0] == 1:
            # The affected device_id
            return result[0][1]
        else:
            # Nothing changed
            return None


    def device_logical_delete(self, device_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_logical_delete(device_name)
        device_name = str(device_name)
        self.cursor.callproc("public.delete_device_logical", [device_name])
        result = self.cursor.fetchall()
        self._print_if_ok("device_logical_delete result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            # The affected device_id
            return result[0][1]
        else:
            # Nothing changed
            return None

    def device_fatal_delete(self, device_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).device_fatal_delete(device_name)
        device_name = str(device_name)
        self.cursor.callproc("public.delete_device_fatal", [device_name])
        result = self.cursor.fetchall()
        self._print_if_ok("device_fatal_delete result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            # The affected device_id
            return result[0][1]
        else:
            # Nothing changed
            return None

    def sku_get(self, device_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).sku_get(device_name)
        self.cursor.callproc("public.get_sku_for_device", [str(device_name)])
        result = self.cursor.fetchall()
        self._print_if_ok("sku_get result: {}".format(result))
        return SqlParser.get_sku_from_results(result)

    def sku_history(self, device_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).sku_history(device_name)
        self.cursor.callproc("public.get_sku_history_device", [device_name])
        result = self.cursor.fetchall()
        self._print_if_ok("sku_history result: {}".format(result))
        return result

    def sku_upsert(self, device_name, sku_name, step=None, hardware_type=None, model_number=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).sku_upsert(device_name, sku_name, step, hardware_type, model_number)
        self.cursor.callproc("public.upsert_sku", [str(device_name), sku_name, step, hardware_type, model_number])
        result = self.cursor.fetchall()
        self._print_if_ok("sku_upsert result: {}".format(result))
        if result is None and result[0][0] != 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        return sku_name

    def sku_delete(self, device_name, sku_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).sku_delete(device_name, sku_name)
        self.cursor.callproc("public.delete_sku", [device_name, sku_name])
        result = self.cursor.fetchall()
        self._print_if_ok("sku_delete result: {}".format(result))
        if result is None and result[0][0] != 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()

    def profile_get(self, profile_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).profile_get(profile_name)
        print("profilename", profile_name)
        self.cursor.callproc("public.get_profile", [profile_name])
        result = self.cursor.fetchall()
        print("result got")
        self._print_if_ok("profile_get result: {}".format(result))
        return SqlParser.get_profile_from_results(result)

    def profile_upsert(self, profile_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).profile_upsert(profile_info)
        profile_name = profile_info.get("profile_name")
        args = SqlParser.prepare_profile_for_query(profile_info)
        self.cursor.callproc("public.upsert_profile", args)
        result = self.cursor.fetchall()
        self._print_if_ok("profile_upsert result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if int(result[0][0]) == 1:
            return profile_name
        else:
            return None

    def profile_delete(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).profile_delete(profile_name)
        self.cursor.callproc("public.delete_profile", [profile_name])
        result = self.cursor.fetchall()
        self._print_if_ok("profile_delete result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        print("profile result {}, {}".format(result[0][0], profile_name))
        if result[0][0] == 1:
            return profile_name
        else:
            return None

    def log_get(self, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).log_get(device_name, limit)
        self.cursor.callproc("public.get_log", [device_name, limit])
        result = self.cursor.fetchall()
        self._print_if_ok("log_get result: {}".format(result))
        return result

    def log_get_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).log_get_timeslice(begin, end, device_name, limit)
        self.cursor.callproc("public.get_log_timeslice", [device_name, limit, begin, end])
        result = self.cursor.fetchall()
        self._print_if_ok("log_get_timeslice result: {}".format(result))
        return result

    def log_add(self, level, msg, device_name=None, process=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).log_add(level, msg, device_name, process)
        self.cursor.callproc("public.add_log", [process, None, level, device_name, msg])
        result = self.cursor.fetchall()
        self._print_if_ok("add_log result: {}".format(result))
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
        self._print_if_ok("configuration_get result: {}".format(result))
        if result is not None and len(result) > 0:
            return result[0][0]
        else:
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
        self._print_if_ok("configuration_upsert result: {}".format(result))
        if result is None or len(result) != 1 or result[0][0] > 1:
            raise DataStoreException("Upsert query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            return key
        else:
            return None

    def configuration_delete(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(PostgresStore, self).configuration_delete(key)
        self.cursor.callproc("public.delete_configuration_value", [str(key)])
        result = self.cursor.fetchall()
        self._print_if_ok("configuration_delete result: {}".format(result))
        if result is None or len(result) > 1 or result[0][0] > 1:
            raise DataStoreException("Delete query affected {} rows, excepted 1".format(result[0][0] if result else 0))
        self.connection.commit()
        if result[0][0] == 1:
            return key
        else:
            return None

    # CANNED QUERIES
    def get_devices_by_type(self, device_type, device_name=None):
        """
                See @DataStore for function description. Only implementation details here.
                """
        # super(PostgresStore, self).get_pdu()
        self.cursor.execute("SELECT * FROM public.get_device_details(%s) WHERE device_type = %s;", [device_name, device_type])
        result = self.cursor.fetchall()
        self._print_if_ok("get_pdu result: {}".format(result))
        return SqlParser.get_device_from_results(result)

    def get_profile_devices(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        # super(PostgresStore, self).get_profile_devices(profile_name)
        self.cursor.callproc("public.get_profile_devices", [profile_name])
        result = self.cursor.fetchall()
        self._print_if_ok("get_profile_devices result: {}".format(result))
        return result


class SqlParser(object):
    """
    Helper class for converting SQL results to objects and objects to SQL params.
    """

    @staticmethod
    def get_device_from_results(results):
        devices = list()
        for result in results:
            print(result)
            device = dict()
            device["device_id"] = result[0]
            device["device_type"] = result[1]
            # device["properties"] = result[2]
            device["hostname"] = result[3]
            device["ip_address"] = result[4]
            device["mac_address"] = result[5]
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
    def get_sku_from_results(results):
        skus = list()
        print("skur results", results)
        for result in results:
            # sku_name character varying
            # hostname character varying
            # ip_address character varying
            # device_type character varying
            sku = dict()
            sku["device_id"] = result[0]
            sku["sku"] = result[1]
            sku["step"] = result[2]
            sku["hardware_type"] = result[3]
            sku["model_number"] = result[4]
            skus.append(sku)
        print("sku list", skus)
        return skus

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
        # Handle a dict
        device = copy.deepcopy(device)
        if not isinstance(device, dict):
            raise RuntimeError("Cannot prepare device of unknown type for query, please pass a dict.")
        device_id = device.pop('device_id', None)
        device_type = device.pop("device_type", None)
        hostname = device.pop("hostname", None)
        ip_address = device.pop("ip_address", None)
        mac_address = device.pop("mac_address", None)
        hardware_type = device.pop("hardware_type", None)
        profile_name = device.pop("profile_name", None)
        return [device_id, device_type, hostname, ip_address, mac_address, hardware_type, profile_name, json.dumps(device)]