# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the FileStore class
"""
from __future__ import print_function
import unittest
from ..filestore import FileStore
from random import randint
from .. import DataStoreException
from dateutil import parser as date_parse
import tempfile
import os


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
          "profile_name": "compute_node",
          "sku": [
            {
              "device_id": 1,
              "hardware_type": "test_hardware2",
              "model_number": 2222,
              "sku": "test_sku_name",
              "step": "test_step2"
            }
          ],
          "deleted": true
        },
        {
          "device_id": 2,
          "device_type": "test_dev_type_test",
          "hostname": "test_hostname2",
          "ip_address": "127.0.0.2",
          "mac_address": "AA:GG:22",
          "profile_name": "compute_node",
          "sku": [
            {
              "device_id": 2,
              "hardware_type": "test_hardware2",
              "model_number": 2222,
              "sku": "test_sku_name",
              "step": "test_step2"
            }
          ],
          "tests": "are_awesome"
        }
      ],
      "profile": [
        {
          "password": "test_pass",
          "port": 22,
          "profile_name": "compute_node"
        }
      ]
    }"""
    LOG_FILENAME = "unknown, setup in setUPCLass(cls)"
    LOG_FILE = """2017-02-22 09:18:54,432 / INFO / DataStore / BATS / None / Does this work?
    2017-01-01 09:18:54,433 / WARNING / DataStore / BATS / None / Does this work?
    2017-01-01 09:18:54,433 / ERROR / DataStore / BATS / None / Does this work?
    2017-01-01 09:18:54,433 / CRITICAL / DataStore / BATS / None / Does this work?
    2017-01-01 09:18:54,434 / INFO / DataStore / None / None / Does this work?
    2017-01-01 09:18:54,434 / WARNING / DataStore / None / None / Does this work?
    2017-01-01 09:18:54,434 / ERROR / DataStore / BATS / None / Does this work?
    2017-01-01 09:18:54,435 / CRITICAL / DataStore / None / None / Does this work?
    2016-01-01 10:25:18,042 / DEBUG / DataStore / BATS / 1 / Does this work?
    2016-01-01 10:25:18,042 / WARNING / DataStore / BATS / 2 / Does this work?
    2015-01-01 10:25:18,042 / ERROR / DataStore / BATS / 1 / Does this work?
    2017-01-01 10:25:18,042 / ERROR / DataStore / Does this work?
    2015-01-01 08:11:25,078 / SKU / DataStore / DataStore / 1 / Inserted: {'sku': '1', 'step': '1', 'device_id': 2}
    2015-01-01 09:18:54,467 / SKU / DataStore / DataStore / 1 / Deleted: {'sku': '1', 'step': '2', 'device_id': 2}
    2015-01-01 14:11:25,078 / SKU / DataStore / DataStore / 2 / Inserted: {'sku': '1', 'step': '1', 'device_id': 2}
    2016-01-01 09:18:54,467 / SKU / DataStore / DataStore / 2 / Updated: {'sku': '1', 'step': '2', 'device_id': 2}
    2017-01-01 09:18:54,467 / SKU / DataStore / DataStore / 2 / Deleted: {'sku': '1', 'step': '2', 'device_id': 2}"""
    
    def setUp(self):
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write(self.FILE_CONFIG)
        temp_file.close()
        self.FILE_STRING = temp_file.name

        temp_log_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_log_file.write(self.LOG_FILE)
        temp_log_file.close()
        self.LOG_FILENAME = temp_log_file.name

        self.fs = FileStore(True, self.FILE_STRING)
        self.fs.configuration_upsert("log_file_path", self.LOG_FILENAME)
        
    def tearDown(self):
        os.remove(self.FILE_STRING)

    def test_file_init(self):
        FileStore(True, self.FILE_STRING)

    def test_device_get(self):
        devices = self.fs.device_get()
        print(devices)
        self.assertEqual(1, len(devices))

        device = self.fs.device_get("test_hostname2")[0]
        self.assertEqual(2, device.get("device_id"))
        
        device = self.fs.device_get("127.0.0.2")[0]
        self.assertEqual(2, device.get("device_id"))

        device = self.fs.device_get(2)[0]
        self.assertEqual(2, device.get("device_id"))

        self.assertEqual("test_hostname2", device.get("hostname"))
        self.assertEqual("compute_node", device.get("profile_name"))
        self.assertEqual(22, device.get("port"))
        self.assertEqual("test_pass", device.get("password"))
        self.assertEqual("are_awesome", device.get("tests"))

        devices = self.fs.device_get("invalid")
        self.assertEqual(0, len(devices))

    def test_device_upsert(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        device_id = self.fs.device_upsert({"device_type": "node", "hostname": "test", "port": num})
        result = self.fs.device_get(device_id)[0]
        self.assertEqual(result.get("port"), num)
        result["port"] = num1
        self.fs.device_upsert(result)
        result = self.fs.device_get(device_id)[0]
        self.assertEqual(result.get("port"), num1)

        result = self.fs.device_get("test_hostname2")[0]
        result["port"] = 153
        self.fs.device_upsert(result)

    def test_device_logical_delete(self):
        # device_id = self.fs.device_upsert({"hostname": "test", "port": 1234})
        device_id = self.fs.device_logical_delete("test")
        if device_id is None:
            # Device Id was None, that means there was no "test" in the devices, add one and try again.
            device_id = self.fs.device_upsert({"device_type": "node", "hostname": "test", "port": 1234})
            device_id = self.fs.device_logical_delete("test")
        self.assertEqual(0, len(self.fs.device_get(device_id)))
        device_id = self.fs.device_logical_delete(device_id)
        self.assertIsNone(device_id)

    def test_device_fatal_delete(self):
        device_id = self.fs.device_fatal_delete("test")
        if device_id is None:
            # Device Id was None, that means there was no "test" in the devices, add one and try again.
            device_id = self.fs.device_upsert({"device_type": "node", "hostname": "test", "port": 1234})
            device_id = self.fs.device_fatal_delete("test")

        self.assertEqual(0, len(self.fs.device_get(device_id)))
        device_id = self.fs.device_fatal_delete(device_id)
        self.assertIsNone(device_id)

    def test_config_get(self):
        self.assertEqual("warewulf", self.fs.configuration_get("provisioning_agent_software"))

    def test_config_upsert(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        self.fs.configuration_upsert("test", num)
        self.assertEqual(num, self.fs.configuration_get("test"))
        self.fs.configuration_upsert("test", num1)
        self.assertEqual(num1, self.fs.configuration_get("test"))

    def test_config_delete(self):
        num = randint(0, 4500000)
        num1 = randint(0, 4500000)
        self.fs.configuration_upsert("test", num)
        self.fs.configuration_delete("test")
        self.assertEqual(None, self.fs.configuration_get("test"))
        self.fs.configuration_upsert("test", num1)
        self.fs.configuration_delete("test")
        self.fs.configuration_delete("test")
        self.fs.configuration_delete("test")
        self.assertEqual(None, self.fs.configuration_get("test"))

    def test_profile_get(self):
        result = self.fs.profile_get()
        self.assertEqual(len(result), 1)
        result = self.fs.profile_get("compute_node")[0]
        self.assertEqual(22, result.get("port"))

        result = self.fs.profile_get("invalid")
        self.assertEqual(0, len(result))

    def test_profile_upsert(self):
        num = randint(0, 4500000)
        self.fs.profile_upsert({"profile_name": "test", "port": num})
        result = self.fs.profile_get("test")[0]
        self.assertEqual(num, result.get("port"))
        result = self.fs.profile_get()
        self.assertEqual(2, len(result))

    def test_profile_delete(self):
        self.fs.profile_delete("compute_node")
        self.assertEqual(self.fs.profile_get("test"), [])
        self.fs.profile_delete("test")
        self.fs.profile_delete("test")
        # Multiple deletes should not throw errors

    def test_log_add(self):
        import logging
        logger = self.fs.get_logger()
        logger.debug("Does this work?", "knl-29", "BATS")
        logger.info("Does this work?", "knl-30", "BATS")
        logger.warning("Does this work?", "knl-31", "BATS")
        logger.error("Does this work?", "knl-33", "BATS")
        logger.critical("Does this work?", "knl-test", "BATS")
        self.fs.log_add(logging.NOTSET, "Does this work?", "knl-test", "BATS")
        logger.debug("Does this work?", None, "BATS")
        logger.info("Does this work?", "knl-test")
        logger.warning("Does this work?", "knl-test", None)
        logger.error("Does this work?", process="BATS")
        logger.critical("Does this work?", device_name="knl-test")
        self.fs.log_add(logging.NOTSET, "Does this work?", "knl-test", "BATS")

    def test_log_get(self):
        result = self.fs.log_get(limit=2)
        print(result[0].get("timestamp"))
        self.assertEqual(2, len(result))
        result = self.fs.log_get(limit=5)
        self.assertEqual(5, len(result))

    def test_sku_get(self):
        result = self.fs.sku_get()
        result = self.fs.sku_get("test_hostname2")
        result = self.fs.sku_get("invalid-29")

    def test_sku_upsert(self):
        result = self.fs.sku_upsert("test_hostname2", "111-asdd-1234-tres")
        result = self.fs.sku_upsert("test_hostname2", "111-asdd-1234-tres", "cpu", "FAT32")

    def test_sku_delete(self):
        num = randint(0, 4500000)
        self.fs.sku_upsert("test_hostname2", "111-asdd-1234-tres", "cpu", num)
        result = self.fs.sku_get("test_hostname2")
        self.assertEqual(2, len(result))

        self.fs.sku_delete("test_hostname2", "111-asdd-1234-tres")
        result = self.fs.sku_get("test_hostname2")
        self.assertEqual(1, len(result))

        self.fs.sku_delete("test_hostname2", "test_sku_name")
        result = self.fs.sku_get("test_hostname2")
        self.assertEqual(0, len(result))

        # No error with multiple deletes
        result = self.fs.sku_delete("test_hostname2", "111-asdd-1234-tres")
        self.assertIsNone(result)
        # No error with bad compute node passed in
        result = self.fs.sku_delete("Not-valid", "11")
        self.assertIsNone(result)

    def test_add_profile_to_device(self):
        self.assertIsNone(self.fs.add_profile_to_device(None))
        result = self.fs.device_get()[0]
        result2 = self.fs.add_profile_to_device(result)
        self.assertTrue(isinstance(result2, list))

    def test_remove_profile_from_device(self):
        self.assertIsNone(self.fs._remove_profile_from_device(None))

    def test_sku_history(self):
        result = self.fs.sku_history("test_hostname2")
        self.assertEqual(3, len(result))
        # TODO: make Postgres and FileStore return the same thing for SKU history!
        print(result)

        result = self.fs.sku_history(1)
        self.assertEqual(2, len(result))

        result = self.fs.sku_history()
        self.assertEqual(5, len(result))

    def test_sku_delete2(self):
        result = self.fs.sku_delete(1, "1")
        self.assertIsNone(result)

        result = self.fs.sku_delete(2, '1')
        self.assertIsNone(result)

    def test_sku_upsert2(self):
        with self.assertRaises(DataStoreException):
            self.fs.sku_upsert(1, '1')

    def test_get_logs(self):
        result = self.fs.log_get()
        self.assertEqual(17, len(result))

        result = self.fs.log_get_timeslice(date_parse.parse("2014-01-01 10:25:18,042"),
                                           date_parse.parse("2016-12-01 10:25:18,042"))
        self.assertEqual(7, len(result))

    def test_get_deleted(self):
        index, device = self.fs._device_find(1, self.fs.parsed_file.get(self.fs.DEVICE_KEY), True)
        self.assertEqual(device.get("device_id"), 1)

    def test_get_by_ip(self):
        index, device = self.fs._device_find("127.0.0.1", self.fs.parsed_file.get(self.fs.DEVICE_KEY), True)
        self.assertEqual(device.get("device_id"), 1)
        result = self.fs.device_get("127.0.0.2")
        self.assertEqual(result[0].get("device_id"), 2)

    def test_config(self):
        result = self.fs.configuration_get("invalid")
        self.assertIsNone(result)

    def test_logger_setup(self):
        self.fs._setup_logger()
        self.fs.logger.handlers = list()
        self.fs._setup_logger()

    def test_device_upsert_id(self):
        self.fs.device_upsert({"device_type": "test_dev_type_test", "hostname": "test_hostname3"})
        result = self.fs.device_get("test_hostname3")
        self.assertEqual(3, result[0].get("device_id"))
        self.fs.device_upsert({"device_type": "test_dev_type_test", "hostname": "test_hostname3", "port": 22, "device_id": 3})
        result = self.fs.device_get("test_hostname3")
        self.assertEqual(3, result[0].get("device_id"))
        self.assertEqual(22, result[0].get("port"))


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
        import os
        os.remove(cls.FILE_STRING)

    def setUp(self):
        print(self.FILE_STRING)
        self.fs = FileStore(True, self.FILE_STRING)

    def test_init(self):
        FileStore(True, self.FILE_STRING)

    def test_empty_gets(self):
        result = self.fs.device_get()
        self.assertEqual(result, [])
        result = self.fs.device_get("there_is_nothing_there")
        self.assertEqual(result, [])
        result = self.fs.profile_get()
        self.assertEqual(result, [])
        result = self.fs.profile_get("there_is_nothing_there")
        self.assertEqual(result, [])
        result = self.fs.configuration_get("there_is_nothing_there")
        self.assertEqual(result, None)
        result = self.fs.sku_get()
        self.assertEqual(result, [])
        result = self.fs.sku_get("there_is_nothing_there")
        self.assertEqual(result, [])

    def test_empty_upserts(self):
        self.fs.device_upsert({"device_type": "node", "hostname": "test"})
        result = self.fs.device_get("test")
        self.assertEqual(result[0].get("hostname"), "test")

        self.fs.profile_upsert({"profile_name": "test", "port": 22})
        result = self.fs.profile_get("test")
        self.assertEqual(result[0].get("profile_name"), "test")

        self.fs.configuration_upsert("test", "value")
        result = self.fs.configuration_get("test")
        self.assertEqual(result, "value")

        self.fs.sku_upsert("test", "1111-2222")
        result = self.fs.sku_get("test")
        self.assertEqual(result[0]["sku"], "1111-2222")

    def test_empty_deletes(self):
        result = self.fs.device_logical_delete("foo")
        self.assertIsNone(result)
        result = self.fs.device_fatal_delete("foo")
        self.assertIsNone(result)
        result = self.fs.profile_delete("foo")
        self.assertIsNone(result)
        result = self.fs.configuration_delete("foo")
        self.assertIsNone(result)
        result = self.fs.sku_delete("foo", "1111-2222")
        self.assertIsNone(result)

@unittest.skip("Tests for future implementation")
class TestFileStoreEmptyFile2(unittest.TestCase):
    FILE_STRING = "unknown, to be constructed in setUpClass(cls)"
    FILE_CONFIG = ""

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
        import os
        os.remove(cls.FILE_STRING)

    def setUp(self):
        print(self.FILE_STRING)
        self.fs = FileStore(True, self.FILE_STRING)

    def test_init(self):
        FileStore(True, self.FILE_STRING)

    def test_empty_gets(self):
        result = self.fs.device_get()
        self.assertEqual(result, [])
        result = self.fs.device_get("there_is_nothing_there")
        self.assertEqual(result, [])
        result = self.fs.profile_get()
        self.assertEqual(result, [])
        result = self.fs.profile_get("there_is_nothing_there")
        self.assertEqual(result, [])
        result = self.fs.configuration_get("there_is_nothing_there")
        self.assertEqual(result, None)
        result = self.fs.sku_get()
        self.assertEqual(result, [])
        result = self.fs.sku_get("there_is_nothing_there")
        self.assertEqual(result, [])

    def test_empty_upserts(self):
        with self.assertRaises(DataStoreException):
            self.fs.sku_upsert("test", "1111-2222")

        self.fs.device_upsert({"device_type": "node", "hostname": "test"})
        result = self.fs.device_get("test")
        self.assertEqual(result[0].get("hostname"), "test")

        self.fs.profile_upsert({"profile_name": "test", "port": 22})
        result = self.fs.profile_get("test")
        self.assertEqual(result[0].get("profile_name"), "test")

        self.fs.configuration_upsert("test", "value")
        result = self.fs.configuration_get("test")
        self.assertEqual(result, "value")

        self.fs.sku_upsert("test", "1111-2222")
        result = self.fs.sku_get("test")
        self.assertEqual(result[0]["sku"], "1111-2222")


    def test_empty_deletes(self):
        result = self.fs.device_logical_delete("foo")
        self.assertIsNone(result)
        result = self.fs.device_fatal_delete("foo")
        self.assertIsNone(result)
        result = self.fs.profile_delete("foo")
        self.assertIsNone(result)
        result = self.fs.configuration_delete("foo")
        self.assertIsNone(result)
        result = self.fs.sku_delete("foo", "1111-2222")
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
        FileStore(False, cls.FILE_STRING).configuration_upsert("log_file_path", cls.LOG_FILENAME)

    @classmethod
    def tearDownClass(cls):
        import os
        os.remove(cls.FILE_STRING)
        os.remove(cls.LOG_FILENAME)

    def setUp(self):
        self.fs = FileStore(True, self.FILE_STRING)

    def test_get_logs(self):
        with self.assertRaises(RuntimeError):
            result = self.fs.log_get()


if __name__ == '__main__':
    unittest.main()
