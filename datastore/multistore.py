# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
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

    def device_get(self, device_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).device_get(device_name)
        results = self._call_function("device_get", [device_name])
        return results[0]

    def device_upsert(self, device_info):
        """
        See @DataStore description
        """
        super(MultiStore, self).device_upsert(device_info)
        results = self._call_function("device_upsert", [device_info])
        return results[0]

    def device_delete(self, device_name):
        """
        See @DataStore description
        """
        super(MultiStore, self).device_delete(device_name)
        results = self._call_function("device_delete", [device_name])
        return results[0]

    def device_history_get(self, device_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).device_history_get(device_name)
        results = self._call_function("device_history_get", [device_name])
        return results[0]

    def profile_get(self, profile_name=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).profile_get(profile_name)
        results = self._call_function("profile_get", [profile_name])
        return results[0]

    def profile_upsert(self, profile_info):
        """
        See @DataStore description
        """
        super(MultiStore, self).profile_upsert(profile_info)
        results = self._call_function("profile_upsert", [profile_info])
        return results[0]

    def profile_delete(self, profile_name):
        """
        See @DataStore description
        """
        super(MultiStore, self).profile_delete(profile_name)
        results = self._call_function("profile_delete", [profile_name])
        return results[0]

    def log_get(self, device_name=None, limit=100):
        """
        See @DataStore description
        """
        super(MultiStore, self).log_get(device_name, limit)
        results = self._call_function("log_get", [device_name, limit])
        return results[0]

    def log_get_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore description
        """
        super(MultiStore, self).log_get_timeslice(begin, end, device_name, limit)
        results = self._call_function("log_get_timeslice", [begin, end, device_name, limit])
        return results[0]

    def log_add(self, level, msg, device_name=None, process=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).log_add(level, process, msg, device_name)
        results = self._call_function("log_add", [level, msg, device_name, process])
        return results[0]

    def configuration_get(self, key=None):
        """
        See @DataStore description
        """
        super(MultiStore, self).configuration_get(key)
        results = self._call_function("configuration_get", [key])
        return results[0]

    def configuration_upsert(self, key, value):
        """
        See @DataStore description
        """
        super(MultiStore, self).configuration_upsert(key, value)
        results = self._call_function("configuration_upsert", [key, value])
        return results[0]

    def configuration_delete(self, key):
        """
        See @DataStore description
        """
        super(MultiStore, self).configuration_delete(key)
        results = self._call_function("configuration_delete", [key])
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
