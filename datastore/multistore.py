# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
For when multiple database are used to store information. Generally this works well for storage but getting from
both databases is generally discouraged.
"""
from .datastore import DataStore, DataStoreException


class MultiStore(DataStore):
    """
    MultiStore performs the same command on all passed DataStore Objects. Then asserts that the results are the same.
    After passing this check the first result is returned.
    """

    def __init__(self, dbs):
        super(MultiStore, self).__init__()
        self.dbs = dbs
        if len(self.dbs) <= 1:
            raise DataStoreException("The MultiStore is designed to be used with multiple databases. "
                                     "Expected > 1 dbs, got {}".format(len(self.dbs)))

    @staticmethod
    def _all_results_equal(results):
        for result1 in results:
            for result2 in results:
                if result1 != result2:
                    raise DataStoreException("Returned results from multiple databases were different. "
                                             "Got {} and {}.".format(result1, result2))

    def _call_function(self, function_name, args):
        results = list()
        for db in self.dbs:
            func = getattr(db, function_name)
            results.append(func(*args))

        self._all_results_equal(results)
        return results

    def get_device(self, device_name):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_device(device_name)
        results = self._call_function("get_device", [device_name])
        return results[0]

    def list_devices(self, filters=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).list_devices(filters)
        results = self._call_function("list_devices", [filters])
        return results[0]

    def set_device(self, device_info):
        """
        See @DataStore description
        """
        super(MultiStore, self).set_device(device_info)
        results = self._call_function("set_device", [device_info])
        return results[0]

    def delete_device(self, device_name):
        """
        See @DataStore description
        """
        super(MultiStore, self).delete_device(device_name)
        results = self._call_function("delete_device", [device_name])
        return results[0]

    def get_device_history(self, device_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_device_history(device_name)
        results = self._call_function("get_device_history", [device_name])
        return results[0]

    def get_profile(self, profile_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_profile(profile_name)
        results = self._call_function("get_profile", [profile_name])
        return results[0]


    def list_profiles(self, filters=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).list_profiles(filters)
        results = self._call_function("list_profiles", [filters])
        return results[0]

    def set_profile(self, profile_info):
        """
        See @DataStore description
        """
        super(MultiStore, self).set_profile(profile_info)
        results = self._call_function("set_profile", [profile_info])
        return results[0]

    def delete_profile(self, profile_name):
        """
        See @DataStore description
        """
        super(MultiStore, self).delete_profile(profile_name)
        results = self._call_function("delete_profile", [profile_name])
        return results[0]

    def list_logs(self, device_name=None, limit=100):
        """
        See @DataStore description
        """
        super(MultiStore, self).list_logs(device_name, limit)
        results = self._call_function("list_logs", [device_name, limit])
        return results[0]

    def list_logs_between_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore description
        """
        super(MultiStore, self).list_logs_between_timeslice(begin, end, device_name, limit)
        results = self._call_function("list_logs_between_timeslice", [begin, end, device_name, limit])
        return results[0]

    def add_log(self, level, msg, device_name=None, process=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).add_log(level, process, msg, device_name)
        results = self._call_function("add_log", [level, msg, device_name, process])
        return results[0]

    def get_configuration_value(self, key=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_configuration_value(key)
        results = self._call_function("get_configuration_value", [key])
        return results[0]

    def list_configuration(self):
        """
        See @DataStore description
        """
        super(MultiStore, self).list_configuration()
        results = self._call_function("list_configuration", [])
        return results[0]

    def set_configuration(self, key, value):
        """
        See @DataStore description
        """
        super(MultiStore, self).set_configuration(key, value)
        results = self._call_function("set_configuration", [key, value])
        return results[0]

    def delete_configuration(self, key):
        """
        See @DataStore description
        """
        super(MultiStore, self).delete_configuration(key)
        results = self._call_function("delete_configuration", [key])
        return results[0]

    # UTIL FUNCTIONS
    def get_device_types(self):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_device_types()
        results = self._call_function("get_device_types", [])
        return results[0]

    def get_log_levels(self):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_log_levels()
        results = self._call_function("get_log_levels", [])
        return results[0]

    # CANNED QUERIES
    def get_node(self, device_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_node()
        results = self._call_function("get_node", [device_name])
        return results[0]

    def get_bmc(self, device_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_bmc()
        results = self._call_function("get_bmc", [device_name])
        return results[0]

    def get_pdu(self, device_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_pdu()
        results = self._call_function("get_pdu", [device_name])
        return results[0]

    def get_profile_devices(self, profile_name):
        """
        See @DataStore description
        """
        super(MultiStore, self).get_profile_devices(profile_name)
        results = self._call_function("get_profile_devices", [profile_name])
        return results[0]

    def export_to_file(self, file_location):
        """
        See @DataStore description
        """
        super(MultiStore, self).export_to_file(file_location)
        results = self._call_function("export_to_file", [file_location])
        return results[0]

    def import_from_file(self, file_location):
        """
        See @DataStore description
        """
        super(MultiStore, self).import_from_file(file_location)
        results = self._call_function("import_from_file", [file_location])
        return results[0]
