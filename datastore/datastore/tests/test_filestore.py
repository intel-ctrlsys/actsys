# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the FileStore class
"""

import unittest
import json
import tempfile
import os
import logging
from ..filestore import FileStore
from random import randint
from .. import DataStoreException
from dateutil import parser as date_parse
from datastore import get_logger, DataStore


class TestFileStore(unittest.TestCase):

    FILE_STRING = "unknown, to be contrusted in setup()"
    FILE_CONFIG = """{
      "configuration_variables": {
        "log_file_path": "/tmp/ctrl.log",
        "provisioning_agent_software": "warewulf"
      },
      "device": [
       {
          "device_id": 1,
          "device_type": "test_dev_type_test",
          "hostname": "test_hostname",
          "ip_address": "127.0.0.1",
          "mac_address": "AA:GG:PP",
          "profile_name": "compute_node"
        },
        {
          "device_id": 2,
          "device_type": "test_dev_type_test",
          "hostname": "test_hostname2",
          "ip_address": "127.0.0.2",
          "mac_address": "AA:GG:22",
          "profile_name": "compute_node",
          "tests": "are_awesome"
        }
      ],
      "profile": [
        {
          "password": "test_pass",
          "port": 22,
          "profile_name": "compute_node"
        }
      ],
      "groups": {
        "test": "@test1,c1,n3",
        "test1": "c99",
        "test2": "c[1-23]"
      }
    }"""
    LOG_FILENAME = "unknown, setup in setUPCLass(cls)"
    LOG_FILE = """2017-02-22 09:18:54,432 / INFO / DataStore / BATS / None / Does this work?;;
    2017-01-01 09:18:54,433 / WARNING / DataStore / BATS / None / Does this work?;;
    2017-01-01 09:18:54,433 / ERROR / DataStore / BATS / None / Does this work?;;
    2017-01-01 09:18:54,433 / CRITICAL / DataStore / BATS / None / Does this work?;;
    2017-01-01 09:18:54,434 / INFO / DataStore / None / None / Does this work?;;
    2017-01-01 09:18:54,434 / WARNING / DataStore / None / None / Does this work?;;
    2017-01-01 09:18:54,434 / ERROR / DataStore / BATS / None / Does this work?;;
    2017-01-01 09:18:54,435 / CRITICAL / DataStore / None / None / Does this work?;;
    2016-01-01 10:25:18,042 / DEBUG / DataStore / BATS / 1 / Does this work?;;
    2016-01-01 10:25:18,042 / WARNING / DataStore / BATS / 2 / Does this work?;;
    2015-01-01 10:25:18,042 / ERROR / DataStore / BATS / 1 / Does this work?;;
    2017-01-01 10:25:18,042 / ERROR / DataStore / Does this work?;;
"""
    FILE_CONFIG_MOCKED = """{
  "configuration_variables": {
    "config": "is_mocked"
  },
  "device": [
    {
      "bmc": "bmc1",
      "debug_ip": "192.168.6.65",
      "debug_port": 65,
      "device_id": 1,
      "device_type": "node",
      "enp60s0_ip_address": "192.168.6.3",
      "hostname": "c1",
      "ip_address": "192.168.6.655",
      "mac_address": "00:00:00:00:00:00",
      "profile_name": "compute_node",
      "provisioner": "UNDEF"
    },
    {
      "bmc": "bmc2",
      "device_id": 2,
      "device_type": "node",
      "hostname": "c2",
      "ip_address": "192.168.1.102",
      "mac_address": "00:00:00:00:00:00",
      "profile_name": "compute_node"
    },
    {
      "device_id": 3,
      "device_type": "bmc",
      "hostname": "bmc1",
      "ip_address": "192.168.2.101",
      "mac_address": "00:00:00:00:00:00",
      "profile_name": "bmc_default"
    },
    {
      "device_id": 4,
      "device_type": "bmc",
      "hostname": "bmc2",
      "ip_address": "192.168.2.102",
      "mac_address": "00:00:00:00:00:00",
      "profile_name": "bmc_default"
    },
    {
      "connected_device": [
        {
          "device": [
            "c1",
            "c2"
          ],
          "outlet": "5"
        }
      ],
      "device_id": 5,
      "device_type": "pdu",
      "hostname": "pdu-1",
      "ip_address": "192.168.3.101",
      "mac_address": "00:00:00:00:00:00",
      "profile_name": "pdu_default"
    }
  ],
  "profile": [
    {
      "access_type": "mock",
      "bmc_boot_timeout_seconds": 1,
      "bmc_chassis_off_wait": 1,
      "image": "centos7.2",
      "os_boot_timeout_seconds": 1,
      "os_network_to_halt_time": 1,
      "os_shutdown_timeout_seconds": 1,
      "password": "password",
      "port": 22,
      "profile_name": "compute_node",
      "provisioner": "mock",
      "resource_controller": "mock",
      "role": [
        "compute"
      ],
      "service_list": [
        "orcmd",
        "gmond"
      ],
      "user": "user",
      "wait_time_after_boot_services": 1
    },
    {
      "access_type": "mock",
      "auth_method": "PASSWORD",
      "channel": 2,
      "password": "password",
      "port": 22,
      "priv_level": "ADMINISTRATOR",
      "profile_name": "bmc_default",
      "type": "bmc",
      "user": "user"
    },
    {
      "access_type": "mock",
      "outlets_count": 8,
      "password": "password",
      "port": 22,
      "profile_name": "pdu_default",
      "type": "pdu",
      "user": "user"
    }
  ],
  "groups": {
    "test": "@test1,c1,n3",
    "test1": "c99",
    "test2": "c[1-23]"
  }
}"""

    def setUp(self):
        temp_log_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_log_file.write(self.LOG_FILE)
        temp_log_file.close()
        self.LOG_FILENAME = temp_log_file.name

        config = json.loads(self.FILE_CONFIG)
        config["configuration_variables"]["log_file_path"] = self.LOG_FILENAME

        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write(json.dumps(config))
        temp_file.close()
        self.FILE_STRING = temp_file.name

        logger = get_logger()
        logger.handlers = []
        DataStore.LOG_LEVEL = logging.DEBUG

        self.fs = FileStore(self.FILE_STRING, None)

    def tearDown(self):
        os.remove(self.FILE_STRING)

    def test_file_init(self):
        FileStore(self.FILE_STRING, None)
        FileStore(self.FILE_STRING, logging.CRITICAL)

        new_file_location = os.path.join(tempfile.gettempdir(), "new_fileStore")

        if os.path.isfile(new_file_location):
            os.remove(new_file_location)
        FileStore(new_file_location)
        self.assertTrue(os.path.isfile(new_file_location))
        os.remove(new_file_location)

    def test_device_get(self):
        devices = self.fs.list_devices()
        print(devices)
        self.assertEqual(2, len(devices))

        device = self.fs.get_device("test_hostname2")
        self.assertEqual(2, device.get("device_id"))
        
        device = self.fs.get_device("127.0.0.2")
        self.assertEqual(2, device.get("device_id"))

        device = self.fs.get_device(2)
        self.assertEqual(2, device.get("device_id"))

        self.assertEqual("test_hostname2", device.get("hostname"))
        self.assertEqual("compute_node", device.get("profile_name"))
        self.assertEqual(22, device.get("port"))
        self.assertEqual("test_pass", device.get("password"))
        self.assertEqual("are_awesome", device.get("tests"))

        devices = self.fs.get_device("not_found_device")
        self.assertIsNone(devices)
        devices = self.fs.list_devices({"foo": "not_found_filter"})
        self.assertEqual(0, len(devices))

    def test_device_upsert(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        device_id = self.fs.set_device({"device_type": "node", "hostname": "test", "port": num})[0]
        result = self.fs.get_device(device_id)
        self.assertEqual(result.get("port"), num)
        result["port"] = num1
        self.fs.set_device(result)
        result = self.fs.get_device(device_id)
        self.assertEqual(result.get("port"), num1)

        result = self.fs.get_device("test_hostname2")
        result["port"] = 153
        self.fs.set_device(result)

    def test_device_delete(self):
        # device_id = self.fs.set_device({"hostname": "test", "port": 1234})
        device_id = self.fs.delete_device("test")
        if device_id is None:
            # Device Id was None, that means there was no "test" in the devices, add one and try again.
            device_id = self.fs.set_device({"device_type": "node", "hostname": "test", "port": 1234})
            device_id = self.fs.delete_device("test")
        self.assertIsNone(self.fs.get_device("test"))
        device_id = self.fs.delete_device(device_id)
        self.assertFalse(device_id)

        device_id = self.fs.delete_device("test")
        if device_id is None:
            # Device Id was None, that means there was no "test" in the devices, add one and try again.
            device_id = self.fs.set_device({"device_type": "node", "hostname": "test", "port": 1234})
            device_id = self.fs.delete_device("test")

        self.assertIsNone(self.fs.get_device("test"))
        device_id = self.fs.delete_device(device_id)
        self.assertFalse(device_id)

    def test_delete_multiple(self):
        self.assertEqual(len(self.fs.list_devices()), 2)
        result = self.fs.delete_device(["test_hostname", "test_hostname2"])
        self.assertListEqual(result, [1, 2])
        self.assertEqual(len(self.fs.list_devices()), 0)
        result = self.fs.delete_device(["test_hostname", "test_hostname2"])
        self.assertListEqual(result, [])
        result = self.fs.delete_device([])
        self.assertListEqual(result, [])

    def test_config_get(self):
        self.assertEqual("warewulf", self.fs.get_configuration_value("provisioning_agent_software"))

    def test_config_upsert(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        self.fs.set_configuration("test", num)
        self.assertEqual(num, self.fs.get_configuration_value("test"))
        self.fs.set_configuration("test", num1)
        self.assertEqual(num1, self.fs.get_configuration_value("test"))

    def test_config_delete(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        self.fs.set_configuration("test", num)
        self.fs.delete_configuration("test")
        self.assertEqual(None, self.fs.get_configuration_value("test"))
        self.fs.set_configuration("test", num1)
        self.fs.delete_configuration("test")
        self.fs.delete_configuration("test")
        self.fs.delete_configuration("test")
        self.assertEqual(None, self.fs.get_configuration_value("test"))

    def test_profile_get(self):
        result = self.fs.list_profiles()
        self.assertEqual(len(result), 1)
        result = self.fs.get_profile("compute_node")
        self.assertEqual(22, result.get("port"))

        result = self.fs.get_profile("invalid")
        self.assertIsNone(result)

    def test_profile_upsert(self):
        num = randint(0, 4500000)
        self.fs.set_profile({"profile_name": "test", "port": num})
        result = self.fs.get_profile("test")
        self.assertEqual(num, result.get("port"))
        result = self.fs.list_profiles()
        self.assertEqual(2, len(result))

    def test_profile_delete(self):
        with self.assertRaises(DataStoreException):
            self.fs.delete_profile("compute_node")
        self.assertIsNone(self.fs.get_profile("test"))
        self.fs.delete_profile("test")
        self.fs.delete_profile("test")
        # Multiple deletes should not throw errors

    def test_log_add(self):
        import logging
        from logging.handlers import RotatingFileHandler
        logger = self.fs.get_logger()
        for index, handler in enumerate(logger.handlers):
            if not isinstance(handler, RotatingFileHandler):
                logger.handlers.pop(index)

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

    def test_log_get(self):
        result = self.fs.list_logs(limit=2)
        print(result[0].get("timestamp"))
        self.assertEqual(2, len(result))
        result = self.fs.list_logs(limit=5)
        self.assertEqual(5, len(result))

    def test_add_profile_to_device(self):
        self.assertIsNone(self.fs.add_profile_to_device(None))
        result = self.fs.list_devices()[0]
        result2 = self.fs.add_profile_to_device(result)
        self.assertTrue(isinstance(result2, list))

    def test_remove_profile_from_device(self):
        self.assertIsNone(self.fs._remove_profile_from_device(None))

    def test_get_logs(self):
        result = self.fs.list_logs()
        self.assertEqual(15, len(result))

        result = self.fs.list_logs_between_timeslice(date_parse.parse("2014-01-01 10:25:18,042+00"),
                                                     date_parse.parse("2016-12-01 10:25:18,042+00"))
        self.assertEqual(3, len(result))

    def test_get_deleted(self):
        index, device = self.fs._device_find(1, self.fs.parsed_file.get(self.fs.DEVICE_KEY))
        self.assertEqual(device.get("device_id"), 1)

    def test_get_by_ip(self):
        index, device = self.fs._device_find("127.0.0.1", self.fs.parsed_file.get(self.fs.DEVICE_KEY))
        self.assertEqual(device.get("device_id"), 1)
        result = self.fs.get_device("127.0.0.2")
        self.assertEqual(result.get("device_id"), 2)

    def test_config(self):
        result = self.fs.get_configuration_value("invalid")
        self.assertIsNone(result)

    def test_logger_setup(self):
        self.fs._setup_file_logger(None)
        self.fs.logger.handlers = list()
        self.fs._setup_file_logger(logging.WARNING)

    def test_device_upsert_id(self):
        self.fs.set_device({"device_type": "test_dev_type_test", "hostname": "test_hostname3"})
        result = self.fs.get_device("test_hostname3")
        self.assertEqual(3, result.get("device_id"))
        self.fs.set_device({"device_type": "test_dev_type_test", "hostname": "test_hostname3", "port": 22, "device_id": 3})
        result = self.fs.get_device("test_hostname3")
        self.assertEqual(3, result.get("device_id"))
        self.assertEqual(22, result.get("port"))

    def test_get_device_by_type(self):
        result = self.fs.get_devices_by_type("test_dev_type_test")
        self.assertEqual(2, len(result))

        result = self.fs.get_devices_by_type("test_dev_type_test", "test_hostname")
        self.assertEqual(1, len(result))

        result = self.fs.get_devices_by_type("Invalid type", "test_hostname")
        self.assertEqual(0, len(result))

    def test_get_profile_devices(self):
        result = self.fs.get_profile_devices("compute_node")
        self.assertEqual(2, len(result))

        result = self.fs.get_profile_devices("Invalid profile")
        self.assertEqual(0, len(result))

    def test_get_device(self):
        device = self.fs.get_device("not-here")
        self.assertIsNone(device)

    def test_invalid_log_level(self):
        with self.assertRaises(DataStoreException):
            self.fs.add_log(1, "not important msg")

        with self.assertRaises(DataStoreException):
            self.fs.set_log_level(1)

        try:
            self.fs.set_log_level(1)
        except DataStoreException as dse:
            print(dse)

    def test_set_log_level(self):
        self.fs.set_log_level(logging.DEBUG)
        self.assertEqual(self.fs.LOG_LEVEL, logging.DEBUG)

        self.fs.set_log_level(logging.CRITICAL)
        self.assertEqual(self.fs.LOG_LEVEL, logging.CRITICAL)

    def test_log_list_msgs(self):
        log_msgs = ["This is a ", "selection of ", "debug msgs"]
        logger = self.fs.get_logger()

        logger.debug(log_msgs)
        logger.info(log_msgs)
        logger.error(log_msgs)
        logger.warning(log_msgs)
        logger.critical(log_msgs)

        logs = self.fs.list_logs()
        self.assertEqual(30, len(logs))

    def test_export_to_file(self):
        file_export_location = os.path.join(tempfile.gettempdir(), 'datastore_export.json')
        self.fs.export_to_file(file_export_location)
        self.assertTrue(os.path.isfile(file_export_location))

        import json
        with open(file_export_location, 'r') as exported_file:
            exported_file_contents = json.load(exported_file)

        self.assertDictEqual(exported_file_contents, self.fs.parsed_file)
        os.remove(file_export_location)

    def test_import_from_file(self):
        import_file = tempfile.NamedTemporaryFile("w", delete=False)
        import_file.write(self.FILE_CONFIG_MOCKED)
        import_file.close()
        self.fs.import_from_file(import_file.name)
        self.assertTrue(os.path.isfile(import_file.name))

        self.assertEqual(len(self.fs.list_devices()), 5)
        self.assertEqual(self.fs.get_configuration_value("config"), "is_mocked")
        os.remove(import_file.name)


    def test_device_history(self):
        with self.assertRaises(DataStoreException):
            self.fs.get_device_history("foo")

    def test_add_log(self):
        self.fs.add_log(logging.WARNING, "This is a test")
        self.fs.add_log(logging.WARNING, "This is a test", "c1")

    def test_list_groups(self):
        result = self.fs.list_groups()
        self.assertEqual(sorted(list(result.keys())), sorted(["test", "test1", "test2"]))

    def test_get_group_devices(self):
        result = self.fs.get_group_devices("test1")
        self.assertEqual(result, "c99")

    def test_add_to_group(self):
        result = self.fs.add_to_group("c98", "test1")
        self.assertEqual(str(result), "c[98-99]")

        result = self.fs.get_group_devices("test1")
        self.assertEqual(str(result), "c[98-99]")

    def test_remove_from_group(self):
        result = self.fs.remove_from_group("c23", "test2")
        self.assertEqual(str(result), "c[1-22]")

        result = self.fs.remove_from_group("c[1-10]", "test2")
        self.assertEqual(str(result), "c[11-22]")

        result = self.fs.remove_from_group("c[1-50]", "test2")
        self.assertEqual(str(result), "")

        try:
            self.fs.remove_from_group("*", "non_existing")
            self.fail()
        except RuntimeError as run_ex:
            self.assertEqual(str(run_ex), "Group non_existing doesn't exist")

        self.assertEqual(len(list(self.fs.get_group_devices("test2"))), 0)


class TestFileStoreEmptyFile(unittest.TestCase):
    FILE_STRING = "unknown, to be constructed in setUpClass(cls)"
    FILE_CONFIG = "{}"

    @classmethod
    def setUpClass(cls):
        # create a file for the class to use
        import tempfile
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write(cls.FILE_CONFIG)
        temp_file.close()
        cls.FILE_STRING = temp_file.name

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.FILE_STRING)

    def setUp(self):
        self.fs = FileStore(self.FILE_STRING, None)

    def test_init(self):
        FileStore(self.FILE_STRING, None)

    def test_empty_gets(self):
        result = self.fs.list_devices()
        self.assertEqual(result, [])
        result = self.fs.get_device("there_is_nothing_there")
        self.assertIsNone(result)
        result = self.fs.list_profiles()
        self.assertEqual(result, [])
        result = self.fs.get_profile("there_is_nothing_there")
        self.assertIsNone(result)
        result = self.fs.get_configuration_value("there_is_nothing_there")
        self.assertEqual(result, None)

    def test_empty_upserts(self):
        self.fs.set_device({"device_type": "node", "hostname": "test"})
        result = self.fs.get_device("test")
        self.assertEqual(result.get("hostname"), "test")

        self.fs.set_profile({"profile_name": "test", "port": 22})
        result = self.fs.get_profile("test")
        self.assertEqual(result.get("profile_name"), "test")

        self.fs.set_configuration("test", "value")
        result = self.fs.get_configuration_value("test")
        self.assertEqual(result, "value")

    def test_empty_deletes(self):
        result = self.fs.delete_device("foo")
        self.assertFalse(result)
        result = self.fs.delete_device("foo")
        self.assertFalse(result)
        result = self.fs.delete_profile("foo")
        self.assertIsNone(result)
        result = self.fs.delete_configuration("foo")
        self.assertIsNone(result)

    def test_group(self):
        try:
            self.fs.remove_from_group("c99", "foo")
            self.fail()
        except RuntimeError as run_ex:
            self.assertEqual(str(run_ex), "Group foo doesn't exist")

        result = self.fs.get_group_devices("test1")
        self.assertEqual(str(result), "")
        self.assertFalse(result)

        result = self.fs.list_groups()
        self.assertEqual(result, {})
        self.assertFalse(result)


        result = self.fs.add_to_group("c98", "test1")
        self.assertEqual(str(result), "c98")

        result = self.fs.get_group_devices("test1")
        self.assertEqual(str(result), "c98")



class TestFileStoreWithNoFile(unittest.TestCase):
    FILE_LOCATION_STRING = "unknown, to be constructed in setUpClass(cls)"

    @classmethod
    def setUpClass(cls):
        # create a file for the class to use
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.close()
        cls.FILE_LOCATION_STRING = temp_file.name
        os.remove(temp_file.name)

    def setUp(self):
        self.fs = FileStore(self.FILE_LOCATION_STRING)

    def tearDown(self):
        if os.path.isfile(self.FILE_LOCATION_STRING):
            os.remove(self.FILE_LOCATION_STRING)

    def test_init(self):
        FileStore(self.FILE_LOCATION_STRING)

    def test_empty_gets(self):
        result = self.fs.list_devices()
        self.assertEqual(result, [])
        result = self.fs.get_device("there_is_nothing_there")
        self.assertIsNone(result)
        result = self.fs.list_profiles()
        self.assertEqual(result, [])
        result = self.fs.get_profile("there_is_nothing_there")
        self.assertIsNone(result)
        result = self.fs.get_configuration_value("there_is_nothing_there")
        self.assertEqual(result, None)

    def test_empty_upserts(self):
        self.fs.set_device({"device_type": "node", "hostname": "test"})
        result = self.fs.get_device("test")
        self.assertEqual(result.get("hostname"), "test")

        self.fs.set_profile({"profile_name": "test", "port": 22})
        result = self.fs.get_profile("test")
        self.assertEqual(result.get("profile_name"), "test")

        self.fs.set_configuration("test", "value")
        result = self.fs.get_configuration_value("test")
        self.assertEqual(result, "value")

    def test_empty_deletes(self):
        result = self.fs.delete_device("foo")
        self.assertFalse(result)
        result = self.fs.delete_device("foo")
        self.assertFalse(result)
        result = self.fs.delete_profile("foo")
        self.assertIsNone(result)
        result = self.fs.delete_configuration("foo")
        self.assertIsNone(result)


class TestFileStoreInvalidLogs(unittest.TestCase):
    FILE_STRING = "unknown, to be constructed in setUpClass(cls)"
    LOG_FILENAME = "unknown, setup in setUPCLass(cls)"
    FILE_CONFIG = """{
  "configuration_variables": {
  },
  "device": [
  ],
  "profile": [
  ]
}"""
    LOG_FILE = """2017-02-22 09:18:54,432 / INFO /
2015-01-01 10:25:18,042 / ERROR / DataStore / BATS / 1 / Does this work?
2017-01-01 10:25:18,042 / ERROR / DataStore / Does this work?
"""

    @classmethod
    def setUpClass(cls):
        # create a file for the class to use
        import tempfile
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write(cls.FILE_CONFIG)
        temp_file.close()
        cls.FILE_STRING = temp_file.name

        temp_log_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_log_file.write(cls.LOG_FILE)
        temp_log_file.close()
        cls.LOG_FILENAME = temp_log_file.name
        FileStore(cls.FILE_STRING, None).set_configuration("log_file_path", cls.LOG_FILENAME)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.FILE_STRING)
        os.remove(cls.LOG_FILENAME)

    def setUp(self):
        self.fs = FileStore(self.FILE_STRING, None)

    def test_get_logs(self):
        with self.assertRaises(RuntimeError):
            result = self.fs.list_logs()

expansion_tests = {
    "accept_lists": ["node1,node2,node3", ["node1", "node2", "node3"]],
    "sequential_numbers": ["node[1-3]", ["node1", "node2", "node3"]],
    "accept_lists2": ["node1,node3", ["node1", "node3"]],
    "comma_seperated_numbers": ["node[1,3]", ["node1", "node3"]],
    "zero_padded_numbers": ["node[01-03]", ["node01", "node02", "node03"]],
    "comma_seperated_lists": ["node[1,45-46,990]", ["node1", "node45", "node46", "node990"]],
}

fold_tests = {
    "lists": ["node1,node2", "node[1-2]"],
    "nosequential_lists": ["node1,node5", "node[1,5]"],
    "nosequential_lists2": ["node1,node12", "node[1,12]"],
    "nosequential_lists3": ["node3,node1", "node[1,3]"],
    "strange_lists": ["node001,node4,node94", "node[001,004,094]"],
    "mutiple_names": ["nhl1,nfl1,nhl2,nfl2", "nfl[1-2],nhl[1-2]"],
    "list1": [["n1", "n2", "n3"], "n[1-3]"],
    "list2": [["n01", "n02", "n03"], "n[01-03]"],
    "list3": [["n1", "n222", "n2"], "n[1-2,222]"],
    "list4": [["n1", "ni2", "nl3"], "n1,ni2,nl3"]
}


class TestNodeExpand(unittest.TestCase):
    FILE_STRING = "unknown, to be constructed in setUpClass(cls)"
    LOG_FILENAME = "unknown, setup in setUPCLass(cls)"
    FILE_CONFIG = """{
      "configuration_variables": {
      },
      "device": [
      ],
      "profile": [
      ]
    }"""
    LOG_FILE = """2017-02-22 09:18:54,432 / INFO /
    2015-01-01 10:25:18,042 / ERROR / DataStore / BATS / 1 / Does this work?
    2017-01-01 10:25:18,042 / ERROR / DataStore / Does this work?
    """

    @classmethod
    def setUpClass(cls):
        # create a file for the class to use
        import tempfile
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write(cls.FILE_CONFIG)
        temp_file.close()
        cls.FILE_STRING = temp_file.name

        temp_log_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_log_file.write(cls.LOG_FILE)
        temp_log_file.close()
        cls.LOG_FILENAME = temp_log_file.name
        FileStore(cls.FILE_STRING, None).set_configuration("log_file_path", cls.LOG_FILENAME)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.FILE_STRING)
        os.remove(cls.LOG_FILENAME)

    def setUp(self):
        self.fs = FileStore(self.FILE_STRING, None)

    def test_expand(self):
        for test_key in list(expansion_tests.keys()):
            test = expansion_tests.get(test_key)
            self.assertEqual(self.fs.expand_device_list(test[0]), test[1])

    def test_fold(self):
        for test_key in list(fold_tests.keys()):
            test = fold_tests.get(test_key)
            self.assertEqual(self.fs.fold_devices(test[0]), test[1])

    def test_empty_expand(self):
        self.assertEqual(self.fs.expand_device_list(None), [])
        self.assertEqual(self.fs.expand_device_list(""), [])

    def test_empty_fold(self):
        self.assertEqual("", self.fs.fold_devices(None))
        self.assertEqual("", self.fs.fold_devices(""))

    def test_invalid_expand(self):
        try:
            self.fs.expand_device_list("[")
            self.fail()
        except self.fs.DeviceListParseError as dlpe:
            self.assertEqual(str(dlpe),  'missing bracket: "["')
            pass

if __name__ == '__main__':
    unittest.main()
