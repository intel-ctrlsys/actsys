# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the RemoteAccessData class
"""
from __future__ import print_function
import unittest
from mock import patch
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
    TEST_POSTGRES_PROFILE = ["compute_node", {
        "password": "test_pass",
        "port": 22,
    }]
    TEST_PROFILE = {
        "password": "test_pass",
        "port": 22,
        "profile_name": "compute_node"
    }
    TEST_POSTGRES_SKU = [1, "1-sku-3-4", "A", "cpu", None, ]
    TEST_SKU = {
        "device_id": 1,
        "sku": "1-sku-3-4",
        "step": "A",
        "hardware_type": "cpu",
        "model_number": None
    }

    def setUp(self):
        self.postgres = None

    def tearDown(self):
        pass

    def set_expected(self, mock_connect, expected):
        self.expected = expected
        mock_connect.return_value.cursor.return_value.fetchall.return_value = expected
        self.postgres = PostgresStore(True, self.CONNECTION_STRING)

    def test_get_device(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE])
        result = self.postgres.get_device('test_hostname')
        self.assertEqual(result, self.TEST_DEVICE)

    def test_device_get(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE, self.TEST_POSTGRES_DEVICE])
        result = self.postgres.device_get()

        self.assertEqual(2, len(result), "Should contain two parsed objects, got {}".format(len(result)))
        self.assertEqual(self.TEST_DEVICE, result[0])

        self.set_expected(mock_connect, [self.TEST_POSTGRES_DEVICE])
        result = self.postgres.device_get(1)
        self.assertEqual(1, len(result), "Should contain one parsed object, got {}".format(len(result)))
        self.assertEqual(self.TEST_DEVICE, result[0])

        self.set_expected(mock_connect, [])
        result = self.postgres.device_get()
        self.assertEqual(0, len(result))

        result = self.postgres.device_get(1)
        self.assertEqual(0, len(result))

    def test_device_upsert(self, mock_connect):
        self.set_expected(mock_connect, [(1, 2)])
        with self.assertRaises(DataStoreException):
            self.postgres.device_upsert({})
        with self.assertRaises(DataStoreException):
            self.postgres.device_upsert({"device_id": 1})

        result = self.postgres.device_upsert({"device_type": "test_device_type", "attr": "is_added"})
        self.assertEqual(result, 2)

        self.set_expected(mock_connect, [(0, 0)])
        result = self.postgres.device_upsert({"device_type": "test_device_type", "attr": "is_added"})
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(5, 5)])
        with self.assertRaises(DataStoreException):
            self.postgres.device_upsert({"device_type": "test_device_type", "attr": "is_added"})

    def test_device_logical_delete(self, mock_connect):
        self.set_expected(mock_connect, [(1, 1)])
        result = self.postgres.device_logical_delete(1)
        self.assertEqual(1, result)

        self.set_expected(mock_connect, [[0, 0]])
        result = self.postgres.device_logical_delete(1)
        self.assertIsNone(result)

        self.set_expected(mock_connect, [[3, 3]])
        with self.assertRaises(DataStoreException):
            result = self.postgres.device_logical_delete(1)

        self.set_expected(mock_connect, [(1, 4)])
        result = self.postgres.device_logical_delete('test')
        self.assertEqual(result, 4)

        self.set_expected(mock_connect, [(0, None)])
        result = self.postgres.device_logical_delete('test')
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(3,)])
        with self.assertRaises(DataStoreException):
            self.postgres.device_logical_delete('test')

    def test_device_fatal_delete(self, mock_connect):
        self.set_expected(mock_connect, [[1, 1]])
        result = self.postgres.device_fatal_delete(1)
        self.assertEqual(1, result)

        self.set_expected(mock_connect, [[0, 0]])
        result = self.postgres.device_fatal_delete(1)
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(3, 3)])
        with self.assertRaises(DataStoreException):
            result = self.postgres.device_fatal_delete(1)

        self.set_expected(mock_connect, [(1, 32)])
        result = self.postgres.device_fatal_delete('node')
        self.assertEqual(result, 32)

        self.set_expected(mock_connect, [(0, None)])
        result = self.postgres.device_fatal_delete('node')
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(3,)])
        with self.assertRaises(DataStoreException):
            self.postgres.device_fatal_delete('node')

    def test_get_sku(self, mock_connect):
        self.set_expected(mock_connect, [self.TEST_POSTGRES_SKU])
        result = self.postgres.sku_get('test')[0]
        self.assertEqual(result, self.TEST_SKU)

        self.set_expected(mock_connect, [])
        result = self.postgres.sku_get()
        self.assertEqual(result, [])

        self.set_expected(mock_connect, [])
        result = self.postgres.sku_get(1)
        self.assertEqual(result, [])

    def test_history_sku(self, mock_connect):
        self.set_expected(mock_connect, [('knl-31', '192.168.1.41', 'node', 'test_step',
                                          'test_hardware', 1234, '2015/10/10')]
                          )
        result = self.postgres.sku_history('test')
        self.assertGreater(len(result), 0)

    def test_sku_upsert(self, mock_connect):
        self.set_expected(mock_connect, [(0, 0)])
        # with self.assertRaises(DataStoreException):
        #     self.postgres.sku_upsert(1, 1)

        self.set_expected(mock_connect, [(0, 1)])
        result = self.postgres.sku_upsert("test_hostname", "foo")

    #     TODO: Finish SKUs

    def test_sku_delete(self, mock_connect):
        pass

    def test_profile_get(self, mock_connect):
        # Single item
        self.set_expected(mock_connect, [self.TEST_POSTGRES_PROFILE])
        result = self.postgres.profile_get('compute_node')
        self.assertEqual(self.TEST_PROFILE, result[0])

        self.set_expected(mock_connect, [self.TEST_POSTGRES_PROFILE, self.TEST_POSTGRES_PROFILE])
        result = self.postgres.profile_get()
        self.assertEqual(2, len(result))

        self.set_expected(mock_connect, [])
        result = self.postgres.profile_get()
        self.assertEqual(result, [])

        self.set_expected(mock_connect, [])
        result = self.postgres.profile_get('compute_node')
        self.assertEqual(result, [])

    def test_profile_upsert(self, mock_connect):
        self.set_expected(mock_connect, [(1,)])
        self.postgres.profile_upsert({"profile_name": "test", "port": 22})

        self.set_expected(mock_connect, [('test_name', {"port": 21})])
        result = self.postgres.profile_get('test_name')

        self.set_expected(mock_connect, [(1, 1)])
        result2 = self.postgres.profile_upsert(result[0])
        self.assertEqual(result2, result[0].get("profile_name"))

        self.set_expected(mock_connect, [(0, 0)])
        result = self.postgres.profile_upsert({"profile_name": "test", "port": 23})
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(55, 55)])
        with self.assertRaises(DataStoreException):
            self.postgres.profile_upsert({"profile_name": "test", "port": 23})

    def test_profile_delete(self, mock_connect):
        self.set_expected(mock_connect, [(1,)])
        self.postgres.profile_delete('test')

        self.set_expected(mock_connect, [(0,)])
        result = self.postgres.profile_delete('test')
        self.assertIsNone(result)

        self.set_expected(mock_connect, [(20,)])
        with self.assertRaises(DataStoreException):
            self.postgres.profile_delete('test')

    def test_log_get(self, mock_connect):
        self.set_expected(mock_connect, [('BAT', None, 50, 112, 'From BAT tests with love.'),
                                         ('BAT', None, 50, 112, 'From BAT tests with love.'),
                                         ('BAT', None, 50, 112, 'From BAT tests with love.')])
        result = self.postgres.log_get()
        self.assertEqual(3, len(result))

    def test_log_get_timeslice(self, mock_connect):
        self.set_expected(mock_connect, [('BAT', datetime.utcnow(), 50, 112, 'From BAT tests with love.'),
                                         ('BAT', datetime.utcnow(), 50, 112, 'From BAT tests with love.'),
                                         ('BAT', datetime.utcnow(), 50, 112, 'From BAT tests with love.')])
        result = self.postgres.log_get_timeslice(datetime.utcnow(), datetime.utcnow() - timedelta(days=1))
        self.assertEqual(3, len(result))

    def test_log_add(self, mock_connect):
        import logging
        self.set_expected(mock_connect, [(1,)])
        postgres = self.postgres
        # Run these and check for execptions
        postgres.log_add(logging.NOTSET, 'From BAT tests with love.')
        postgres.log_add(logging.DEBUG, 'From BAT tests with love.', None, "BAT")
        postgres.log_add(logging.INFO, 'From BAT tests with love.', "test_hostname")
        postgres.log_add(logging.WARNING, 'From BAT tests with love.', "test_ip_address")
        postgres.log_add(logging.ERROR, 'From BAT tests with love.', "test_hostname", "BAT")
        postgres.log_add(logging.CRITICAL, 'From BAT tests with love.', "test_ip_address", "BAT")

        self.set_expected(mock_connect, [(0,)])
        with self.assertRaises(DataStoreException):
            postgres.log_add(logging.CRITICAL, 'From BAT tests with love.', "test_ip_address", "BAT")

    def test_config_get(self, mock_connect):
        self.set_expected(mock_connect, [['bar']])
        result = self.postgres.configuration_get('foo')
        self.assertEqual(result, 'bar')

        self.set_expected(mock_connect, [])
        result = self.postgres.configuration_get('foo')
        self.assertIsNone(result)

    def test_config_upsert(self, mock_connect):
        self.set_expected(mock_connect, [])
        with self.assertRaises(DataStoreException):
            self.postgres.configuration_upsert('foo', 'bar')

        self.set_expected(mock_connect, [[1]])
        result = self.postgres.configuration_upsert('foo', 'bar')
        self.assertEqual(result, 'foo')

    def test_config_delete(self, mock_connect):
        self.set_expected(mock_connect, [[1]])
        result = self.postgres.configuration_delete('foo')
        self.assertEqual(result, 'foo')

        self.set_expected(mock_connect, [[0]])
        result = self.postgres.configuration_delete('foo')
        self.assertIsNone(result)

        self.set_expected(mock_connect, [[5]])
        with self.assertRaises(DataStoreException):
            self.postgres.configuration_delete('foo')

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

if __name__ == '__main__':
    unittest.main()
