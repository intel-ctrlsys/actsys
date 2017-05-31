# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the RemoteAccessData class
"""
from __future__ import print_function
import unittest
import tempfile
import os
from mock import patch, MagicMock
from ..postgresstore import PostgresStore
from ..datastore import DataStoreException
from random import randint
from datetime import datetime, timedelta


@patch("psycopg2.connect")
class TestPostgresDB(unittest.TestCase):
    """Simple tests for a simple class."""

    CONNECTION_STRING = "host=abc port=1234 dbname=foo user=foo password=foo"
    TEST_POSTGRES_DEVICE = [1, "test_device_type", {"tests": "are_awesome"}, "test_hostname", "127.0.0.1",
                            "AA:GG:11", "compute_node", {"password": "test_pass", "port": 22}]
    TEST_DEVICE = {
        "device_id": 1,
        "device_type": "test_device_type",
        "hostname": "test_hostname",
        "ip_address": "127.0.0.1",
        "mac_address": "AA:GG:11",
        "profile_name": "compute_node",
        "tests": "are_awesome",
        "password": "test_pass",
        "port": 22,
    }
    TEST_POSTGRES_DEVICE2 = [2, "test_device_type2", {"tests": "are_awesome2"}, "test_hostname2", "127.0.0.2",
                             "AA:GG:22", "invalid_profile", {"password": "test_pass2", "port": 222}]
    TEST_DEVICE2 = {
        "device_id": 2,
        "device_type": "test_device_type2",
        "hostname": "test_hostname2",
        "ip_address": "127.0.0.2",
        "mac_address": "AA:GG:22",
        "profile_name": "invalid_profile",
        "tests": "are_awesome2",
        "password": "test_pass2",
        "port": 222,
    }
    TEST_POSTGRES_PROFILE = ["compute_node", {
        "password": "test_pass",
        "port": 22,
    }]
    TEST_PROFILE = {
        "password": "test_pass",
        "port": 22,
        "profile_name": "compute_node"
    }
    TEST_CONFIG = {
        "key": "config",
        "value": "is_mocked"
    }

    def setUp(self):
        self.postgres = None

    def tearDown(self):
        pass

    def func(self, *args):
        pass

    def set_expected(self, mock_connect, expected):
        self.expected = expected
        mock_connect.return_value.cursor.return_value.fetchall.return_value = expected
        self.postgres = PostgresStore(self.CONNECTION_STRING, None)
        self.log_add_org = self.postgres.add_log
        self.postgres.add_log = self.func

    def test_connect(self, mock_connect):
        self.set_expected(mock_connect, [])
        self.postgres.connect()
        setattr(self.postgres, "cursor", None)
        self.postgres.connect()

    def test_get_device(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE])
        result = self.postgres.get_device('test_hostname')
        self.assertEqual(result, self.TEST_DEVICE)

    def test_device_get(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE, self.TEST_POSTGRES_DEVICE])
        result = self.postgres.list_devices()

        self.assertEqual(2, len(result), "Should contain two parsed objects, got {}".format(len(result)))
        self.assertEqual(self.TEST_DEVICE, result[0])

        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE])
        result = self.postgres.get_device(1)
        self.assertEqual(self.TEST_DEVICE, result)

        self.set_expected(mock_connect, [])
        result = self.postgres.list_devices()
        self.assertEqual(0, len(result))

        result = self.postgres.get_device(1)
        self.assertIsNone(result)

    def test_device_list_filter(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE, self.TEST_POSTGRES_DEVICE2])
        result = self.postgres.list_devices({"password": "test_pass"})

        self.assertEqual(1, len(result))
        self.assertEqual(result[0], self.TEST_DEVICE)

        result = self.postgres.list_devices({"port": 222})

        self.assertEqual(1, len(result))
        self.assertEqual(result[0], self.TEST_DEVICE2)

    def test_device_upsert(self, mock_connect):
        self.set_expected(mock_connect, [(1, 2, None, None, None, None, None, None, None)])
        with self.assertRaises(DataStoreException):
            self.postgres.set_device({})
        with self.assertRaises(DataStoreException):
            self.postgres.set_device({"device_id": 1})

        result = self.postgres.set_device({"device_type": "test_device_type", "attr": "is_added"})
        self.assertEqual(result, [2])

        self.set_expected(mock_connect, [(0, 0, None, None, None, None, None, None, None)])
        with self.assertRaises(DataStoreException):
            # Exception due to nothing being updated... Something should always be updated.
            self.postgres.set_device({"device_type": "test_device_type", "attr": "is_added"})

        self.set_expected(mock_connect, [(5, 5, None, None, None, None, None, None, None)])
        with self.assertRaises(DataStoreException):
            # Exception due to too many things being updated, only one should of been updated.
            self.postgres.set_device({"device_type": "test_device_type", "attr": "is_added"})

    def assertListEmpty(self, pList):
        self.assertListEqual(pList, [])

    def test_device_delete(self, mock_connect):
        self.set_expected(mock_connect, [(1, 1)])
        result = self.postgres.delete_device(1)
        self.assertEqual([1], result)

        self.set_expected(mock_connect, [[0, 0]])
        result = self.postgres.delete_device(1)
        self.assertListEmpty(result)

        self.set_expected(mock_connect, [[3, 3]])
        with self.assertRaises(DataStoreException):
            result = self.postgres.delete_device(1)

        self.set_expected(mock_connect, [(1, 4)])
        result = self.postgres.delete_device('test')
        self.assertEqual(result, [4])

        self.set_expected(mock_connect, [(0, None)])
        result = self.postgres.delete_device('test')
        self.assertListEmpty(result)

        self.set_expected(mock_connect, [(3,)])
        with self.assertRaises(DataStoreException):
            self.postgres.delete_device('test')

        self.set_expected(mock_connect, [[1, 1]])
        result = self.postgres.delete_device(1)
        self.assertEqual([1], result)

        self.set_expected(mock_connect, [[0, 0]])
        result = self.postgres.delete_device(1)
        self.assertListEmpty(result)

        self.set_expected(mock_connect, [(3, 3)])
        with self.assertRaises(DataStoreException):
            result = self.postgres.delete_device(1)

        self.set_expected(mock_connect, [(1, 32)])
        result = self.postgres.delete_device('node')
        self.assertEqual(result, [32])

        self.set_expected(mock_connect, [(0, None)])
        result = self.postgres.delete_device('node')
        self.assertListEmpty(result)

        self.set_expected(mock_connect, [(3,)])
        with self.assertRaises(DataStoreException):
            self.postgres.delete_device('node')

    def test_get_device_history(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE])
        result = self.postgres.get_device_history()
        self.assertEqual(result, [self.TEST_DEVICE])

        result = self.postgres.get_device_history(self.TEST_DEVICE.get("hostname"))
        self.assertEqual(result, [self.TEST_DEVICE])

    def test_profile_get(self, mock_connect):
        # Single item
        self.set_expected(mock_connect, [self.TEST_POSTGRES_PROFILE])
        result = self.postgres.get_profile('compute_node')
        self.assertEqual(self.TEST_PROFILE, result)

        self.set_expected(mock_connect, [self.TEST_POSTGRES_PROFILE, self.TEST_POSTGRES_PROFILE])
        result = self.postgres.list_profiles()
        self.assertEqual(2, len(result))

        self.set_expected(mock_connect, [])
        result = self.postgres.list_profiles()
        self.assertEqual(result, [])

        self.set_expected(mock_connect, [])
        result = self.postgres.get_profile('compute_node')
        self.assertIsNone(result)

    def test_profile_upsert(self, mock_connect):
        self.set_expected(mock_connect, [(1,)])
        self.postgres.set_profile({"profile_name": "test", "port": 22})

        self.set_expected(mock_connect, [('test_name', {"port": 21})])
        result = self.postgres.get_profile('test_name')

        self.set_expected(mock_connect, [(1, 1)])
        result2 = self.postgres.set_profile(result)
        self.assertEqual(result2, result.get("profile_name"))

        self.set_expected(mock_connect, [(0, 0)])
        result = self.postgres.set_profile({"profile_name": "test", "port": 23})
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(55, 55)])
        with self.assertRaises(DataStoreException):
            self.postgres.set_profile({"profile_name": "test", "port": 23})

        with self.assertRaises(DataStoreException):
            self.postgres.set_profile({"port": 24})

    def test_profile_delete(self, mock_connect):
        def fake_devices(profile_name):
            return []

        self.set_expected(mock_connect, [(1,)])
        self.postgres.get_profile_devices = fake_devices
        self.postgres.delete_profile('test')

        self.set_expected(mock_connect, [(0,)])
        self.postgres.get_profile_devices = fake_devices
        result = self.postgres.delete_profile('test')
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(20,)])
        self.postgres.get_profile_devices = fake_devices
        with self.assertRaises(DataStoreException):
            self.postgres.delete_profile('test')

    def test_log_get(self, mock_connect):
        self.set_expected(mock_connect, [('BAT', None, 50, 112, 'From BAT tests with love.'),
                                         ('BAT', None, 50, 112, 'From BAT tests with love.'),
                                         ('BAT', None, 50, 112, 'From BAT tests with love.')])
        result = self.postgres.list_logs()
        self.assertEqual(3, len(result))

    def test_log_get_timeslice(self, mock_connect):
        self.set_expected(mock_connect, [('BAT', datetime.utcnow(), 50, 112, 'From BAT tests with love.'),
                                         ('BAT', datetime.utcnow(), 50, 112, 'From BAT tests with love.'),
                                         ('BAT', datetime.utcnow(), 50, 112, 'From BAT tests with love.')])
        result = self.postgres.list_logs_between_timeslice(datetime.utcnow(), datetime.utcnow() - timedelta(days=1))
        self.assertEqual(3, len(result))

    def test_log_add(self, mock_connect):
        import logging
        self.set_expected(mock_connect, [(1,)])
        self.postgres.add_log = self.log_add_org
        postgres = self.postgres
        # Run these and check for execptions
        postgres.add_log(logging.DEBUG, 'From BAT tests with love.', None, "BAT")
        postgres.add_log(logging.INFO, 'From BAT tests with love.', "test_hostname")
        postgres.add_log(logging.WARNING, 'From BAT tests with love.', "test_ip_address")
        postgres.add_log(logging.ERROR, 'From BAT tests with love.', "test_hostname", "BAT")
        postgres.add_log(logging.CRITICAL, 'From BAT tests with love.', "test_ip_address", "BAT")

        self.set_expected(mock_connect, [(5,)])
        self.postgres.add_log = self.log_add_org
        with self.assertRaises(DataStoreException):
            postgres.add_log(logging.CRITICAL, 'From BAT tests with love.', "test_ip_address", "BAT")

        self.set_expected(mock_connect, [(1,)])
        self.postgres.add_log = self.log_add_org
        self.logger = self.postgres.get_logger()
        self.logger.critical('From BAT tests with love')
        self.logger.error('From BAT tests with love')
        self.logger.warning('From BAT tests with love')
        self.logger.info('From BAT tests with love', None, "BAT")
        self.logger.debug('From BAT tests with love', "test_hostname")

        self.logger.journal('command_name', command_result='From BAT tests with love')
        self.logger.journal('command_name', ['a', 'b', 'c', 'd'], 'From BAT tests with love')

    def test_config_get(self, mock_connect):
        self.set_expected(mock_connect, [['bar']])
        result = self.postgres.get_configuration_value('foo')
        self.assertEqual(result, 'bar')

        self.set_expected(mock_connect, [])
        result = self.postgres.get_configuration_value('foo')
        self.assertIsNone(result)

    def test_config_upsert(self, mock_connect):
        self.set_expected(mock_connect, [])
        with self.assertRaises(DataStoreException):
            self.postgres.set_configuration('foo', 'bar')

        self.set_expected(mock_connect, [[1]])
        result = self.postgres.set_configuration('foo', 'bar')
        self.assertEqual(result, 'foo')

    def test_config_delete(self, mock_connect):
        self.set_expected(mock_connect, [[1]])
        result = self.postgres.delete_configuration('foo')
        self.assertEqual(result, 'foo')

        self.set_expected(mock_connect, [[0]])
        result = self.postgres.delete_configuration('foo')
        self.assertIsNone(result)

        self.set_expected(mock_connect, [[5]])
        with self.assertRaises(DataStoreException):
            self.postgres.delete_configuration('foo')

    def test_get_node(self, mock_connect):
        self.set_expected(mock_connect, [[1, "node", {"password": "bar"}, "hostname", "ip_address",
                                          "mac_address", "profile_name", {"port": 21}]])
        result = self.postgres.get_node()
        self.assertEqual(len(result), 1)

        result = self.postgres.get_node(1)
        self.assertEqual(len(result), 1)

    def test_get_bmc(self, mock_connect):
        self.set_expected(mock_connect, [[1, "bmc", {"password": "bar"}, "hostname", "ip_address",
                                          "mac_address", "profile_name", {"port": 21}]])
        result = self.postgres.get_bmc()
        self.assertEqual(len(result), 1)

    def test_get_psu(self, mock_connect):
        self.set_expected(mock_connect, [[1, "psu", {"password": "bar"}, "hostname", "ip_address",
                                          "mac_address", "profile_name", {"port": 21}]])
        result = self.postgres.get_psu()
        self.assertEqual(len(result), 1)

    def test_get_pdu(self, mock_connect):
        self.set_expected(mock_connect, [[1, "pdu", {"password": "bar"}, "hostname", "ip_address",
                                          "mac_address", "profile_name", {"port": 21}]])
        result = self.postgres.get_pdu()
        self.assertEqual(len(result), 1)

    def test_get_profile_devices(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE, self.TEST_POSTGRES_DEVICE,
                                         self.TEST_POSTGRES_DEVICE, self.TEST_POSTGRES_DEVICE])
        result = self.postgres.get_profile_devices("compute_node")
        self.assertEqual(4, len(result))

    def test_get_device_types(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE, self.TEST_POSTGRES_DEVICE2])
        result = self.postgres.get_device_types()
        self.assertEqual(result, ["test_device_type", "test_device_type2"])

        self.set_expected(mock_connect, [])
        result = self.postgres.get_device_types()
        self.assertEqual(result, [])

    def test_export_to_file(self, mock_connect):
        expected_export_json = {
            'device': [
                {'mac_address': '6', 'hostname': '4', 'ip_address': '5', 'device_type': {}, 'device_id': u'1'}
            ],
            'profile': [
                {'profile_name': '1'}
            ],
            'configuration_variables': {
                '1': {},
                'log_file_path': '/tmp/datastore_export.json.log'
            }
        }
        self.set_expected(mock_connect, [["1", {}, None, "4", "5", "6", None, None]])

        file_export_location = os.path.join(tempfile.gettempdir(), 'datastore_export.json')
        self.postgres.export_to_file(file_export_location)
        self.assertTrue(os.path.isfile(file_export_location))

        import json
        with open(file_export_location, 'r') as exported_file:
            exported_file_contents = json.load(exported_file)

        print(exported_file_contents)
        self.assertDictEqual(exported_file_contents, expected_export_json)
        os.remove(file_export_location)

    def test_import_from_file(self, mock_connect):
        self.set_expected(mock_connect, [])
        import_file = tempfile.NamedTemporaryFile("w", delete=False)
        import_file.write("{}")
        import_file.close()
        self.postgres.import_from_file(import_file.name)
        os.remove(import_file.name)

    def test_import_from_file_failure(self, mock_connect):
        file_config = """{
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
              ]
            }"""
        postgres = MagicMock(spec=PostgresStore)
        PostgresStore.__init__(postgres, "", 10)
        postgres._delete_database.return_value = [self.TEST_CONFIG], [self.TEST_DEVICE], [self.TEST_PROFILE]
        postgres.set_device.side_effect = [Exception("The mocked exception"), None]

        import_file = tempfile.NamedTemporaryFile("w", delete=False)
        import_file.write(file_config)
        import_file.close()

        try:
            PostgresStore.import_from_file(postgres, import_file.name)
            self.fail()
        except Exception as ex:
            self.assertEqual(ex.message, "The mocked exception")

        os.remove(import_file.name)

    def test_database_delete(self, mock_connect):
        self.set_expected(mock_connect, [])
        old_config, old_devices, old_profiles = self.postgres._delete_database()
        self.assertListEqual(old_config, [])
        self.assertListEqual(old_devices, [])
        self.assertListEqual(old_profiles, [])

if __name__ == '__main__':
    unittest.main()
