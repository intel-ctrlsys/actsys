# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
from __future__ import print_function
import unittest
from ..datastore import DataStore, DataStoreException
from ..multistore import MultiStore
from random import randint
from mock import MagicMock


class TestMultiStore(unittest.TestCase):
    """
    This test simply runs the functions supplied, the check is done by MultiStore itself. This MultiStore test isn't
    really concerned with the output from the functions, only that they are the same across multiple DataStore impl.
    """

    def setUp(self):
        self.fs = MagicMock(spec=DataStore)
        self.ps = self.fs
        self.ms = MultiStore([self.fs, self.ps])

    def test_init(self):
        with self.assertRaises(DataStoreException):
            MultiStore([])

        with self.assertRaises(DataStoreException):
            MultiStore([])

        with self.assertRaises(DataStoreException):
            MultiStore([self.fs])

        with self.assertRaises(DataStoreException):
            MultiStore([self.fs])

    def test_all_results_equal(self):
        self.ms._all_results_equal(["foo", "foo"])
        self.ms._all_results_equal([1, 1])
        self.ms._all_results_equal([{}, {}])
        self.ms._all_results_equal([{"foo": "bar"}, {"foo": "bar"}])
        self.ms._all_results_equal([[], []])
        self.ms._all_results_equal([[1, 2, "r"], [1, 2, "r"]])
        self.ms._all_results_equal([["t", 1, 2], ["t", 1, 2]])
        self.ms._all_results_equal([[{}], [{}]])
        self.ms._all_results_equal([[{"foo": "bar", "1": 2}], [{"foo": "bar", "1": 2}]])

    def test_call_function(self):
        test_func = MagicMock()
        # DataStore.test_func = classmethod(test_func)
        self.fs.test_func = test_func
        self.ms._call_function("test_func", [1, 2, 3])
        self.assertEqual(test_func.call_count, 2)

    def test_get_device(self):
        self.ms.get_device("compute-29")

    def test_list_devices(self):
        self.ms.list_devices()
        self.ms.list_devices({"hostname": "not-valid"})
        self.ms.list_devices({"hostname": "compute-29"})

    def test_device_upsert(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        with self.assertRaises(DataStoreException):
            self.ms.set_device({"hostname": "test", "port": num})
        self.ms.set_device({"device_type": "node", "hostname": "test", "port": num})
        self.ms.set_device({"device_type": "node", "hostname": "test", "port": num1})

    def test_device_delete(self):
        self.ms.set_device({"device_type": "node", "hostname": "test", "port": 123})
        self.ms.delete_device("test")
        self.ms.delete_device("test")

        self.ms.set_device({"device_type": "node", "hostname": "test", "port": 123})
        self.ms.delete_device("test")
        self.ms.delete_device("test")

    def test_get_device_history(self):
        self.ms.get_device_history()
        self.ms.get_device_history("compute-29")

    def test_get_profile(self):
        self.ms.get_profile("invalid")
        self.ms.get_profile("compute-29")

    def test_list_profiles(self):
        self.ms.list_profiles()

    def test_profile_upsert(self):
        num = randint(0, 4500000)
        self.ms.set_profile({"profile_name": "test", "port": num})

    def test_profile_delete(self):
        self.ms.set_profile({"profile_name": "test", "port": 123})
        self.ms.delete_profile("invalid")
        self.ms.delete_profile("test")
        self.ms.delete_profile("test")

    def test_log_get(self):
        self.ms.list_logs(limit=2)
        self.ms.list_logs("invalid")
        self.ms.list_logs("compute-29")

    def test_add_log(self):
        self.fs.get_log_levels.return_value = [DataStore.LOG_LEVEL_WARNING]
        self.ms.add_log(DataStore.LOG_LEVEL_WARNING, "foo")

    def test_log_get_timeslice(self):
        from datetime import datetime, timedelta
        result = self.ms.list_logs_between_timeslice(datetime.utcnow() - timedelta(days=5 * 365),
                                                     datetime.utcnow() - timedelta(days=300))

    def test_log_add(self):
        import logging
        logger = self.ms.get_logger()
        logger.debug("Does this work?", "knl-29", "BATS")
        logger.info("Does this work?", "knl-30", "BATS")
        logger.warning("Does this work?", "knl-31", "BATS")
        logger.error("Does this work?", "knl-33", "BATS")
        logger.critical("Does this work?", "knl-test", "BATS")
        logger.debug("Does this work?", None, "BATS")
        logger.info("Does this work?", "knl-test")
        logger.warning("Does this work?", "knl-test", None)
        logger.error("Does this work?")
        logger.critical("Does this work?", device_name="knl-test")

    def test_configuration_get_value(self):
        self.ms.get_configuration_value()
        self.ms.get_configuration_value("invalid")
        self.ms.get_configuration_value("provisioning_agent_software")

    def test_list_configuration(self):
        self.ms.list_configuration()

    def test_configuration_upsert(self):
        num = randint(0, 4500000)
        self.ms.set_configuration("test", num)
        self.fs.set_configuration("test", num)

    def test_configuration_delete(self):
        self.ms.set_configuration("test", 123)
        self.ms.delete_configuration("test")
        self.ms.delete_configuration("test")
        self.ms.delete_configuration("invalid")

    # UTIL FUNCTIONS
    def test_get_device_types(self):
        self.ms.get_device_types()

    def test_get_log_levels(self):
        self.ms.get_log_levels()
        pass

    # CANNED QUERIES
    def test_get_node(self):
        self.ms.get_node()

    def test_get_bmc(self):
        self.ms.get_bmc()

    def test_get_pdu(self):
        self.ms.get_pdu()

    def test_get_profile_devices(self):
        self.ms.get_profile_devices("test")
        self.ms.get_profile_devices("compute Node")
