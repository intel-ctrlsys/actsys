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
        self.ms = MultiStore(True, [self.fs, self.ps])

    def test_init(self):
        with self.assertRaises(DataStoreException):
            MultiStore(True, [])

        with self.assertRaises(DataStoreException):
            MultiStore(False, [])

        with self.assertRaises(DataStoreException):
            MultiStore(True, [self.fs])

        with self.assertRaises(DataStoreException):
            MultiStore(False, [self.fs])

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

    def test_device_get(self):
        self.ms.device_get()
        self.ms.device_get("not-valid")
        self.ms.device_get("compute-29")

    def test_device_upsert(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        with self.assertRaises(DataStoreException):
            self.ms.device_upsert({"hostname": "test", "port": num})
        self.ms.device_upsert({"device_type": "node", "hostname": "test", "port": num})
        self.ms.device_upsert({"device_type": "node", "hostname": "test", "port": num1})

    def test_device_logical_delete(self):
        self.ms.device_upsert({"device_type": "node", "hostname": "test", "port": 123})
        self.ms.device_logical_delete("test")
        self.ms.device_logical_delete("test")

    def test_device_fatal_delete(self):
        self.ms.device_upsert({"device_type": "node", "hostname": "test", "port": 123})
        self.ms.device_fatal_delete("test")
        self.ms.device_fatal_delete("test")

    def test_sku_get(self):
        self.ms.sku_get()
        self.ms.sku_get("invalid")
        self.ms.sku_get("compute-29")

    def test_sku_history(self):
        self.ms.sku_history()
        self.ms.sku_history("invalid")
        self.ms.sku_history("compute-29")

    def test_sku_upsert(self):
        self.ms.sku_upsert("invalid", "111-asdd-1234-tres")
        self.ms.sku_upsert("compute-29", "111-asdd-1234-tres")
        self.ms.sku_upsert("compute-29", "111-asdd-1234-tres", "cpu", "FAT32")

    def test_sku_delete(self):
        self.ms.sku_upsert("invalid", "111-asdd-1234-tres")
        self.ms.sku_delete("compute-29", "invalid")
        self.ms.sku_delete("compute-29", "111-asdd-1234-tres")
        self.ms.sku_delete("compute-29", "111-asdd-1234-tres")

    def test_profile_get(self):
        self.ms.profile_get()
        self.ms.profile_get("invalid")
        self.ms.profile_get("compute-29")

    def test_profile_upsert(self):
        num = randint(0, 4500000)
        self.ms.profile_upsert({"profile_name": "test", "port": num})

    def test_profile_delete(self):
        self.ms.profile_upsert({"profile_name": "test", "port": 123})
        self.ms.profile_delete("invalid")
        self.ms.profile_delete("test")
        self.ms.profile_delete("test")

    def test_log_get(self):
        self.ms.log_get(limit=2)
        self.ms.log_get("invalid")
        self.ms.log_get("compute-29")

    def test_log_get_timeslice(self):
        from datetime import datetime, timedelta
        result = self.ms.log_get_timeslice(datetime.utcnow() - timedelta(days=5 * 365),
                                           datetime.utcnow() - timedelta(days=300))

    def test_log_add(self):
        import logging
        logger = self.ms.get_logger()
        logger.debug("Does this work?", "knl-29", "BATS")
        logger.info("Does this work?", "knl-30", "BATS")
        logger.warning("Does this work?", "knl-31", "BATS")
        logger.error("Does this work?", "knl-33", "BATS")
        logger.critical("Does this work?", "knl-test", "BATS")
        self.ms.log_add(logging.NOTSET, "Does this work?", "knl-test", "BATS")
        logger.debug("Does this work?", None, "BATS")
        logger.info("Does this work?", "knl-test")
        logger.warning("Does this work?", "knl-test", None)
        logger.error("Does this work?", process="BATS")
        logger.critical("Does this work?", device_name="knl-test")
        self.ms.log_add(logging.NOTSET, "Does this work?", "knl-test", "BATS")

    def test_configuration_get(self):
        self.ms.configuration_get()
        self.ms.configuration_get("invalid")
        self.ms.configuration_get("provisioning_agent_software")

    def test_configuration_upsert(self):
        num = randint(0, 4500000)
        self.ms.configuration_upsert("test", num)
        self.fs.configuration_upsert("test", num)

    def test_configuration_delete(self):
        self.ms.configuration_upsert("test", 123)
        self.ms.configuration_delete("test")
        self.ms.configuration_delete("test")
        self.ms.configuration_delete("invalid")

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
