# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the FileStore class
"""
from __future__ import print_function
from mock import MagicMock, Mock, patch
import unittest
import io
import StringIO
import sys
from ..datastore import DataStore
from ..DataStoreCLI import DataStoreCLI
from random import randint


class TestDataStoreCLI(unittest.TestCase):

    def setUp(self):
        self.mockDS = Mock(spec=DataStore)
        self.dscli = DataStoreCLI(self.mockDS)


    def test_datastoreCLI_init(self):
        result = DataStoreCLI(self.mockDS)
        self.assertIsNotNone(result)

    def test_device_list(self):
        self.mockDS.device_get.return_value = [{'hostname': 'node1'}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['device', 'list'])
            self.assertEqual(output.getvalue(), '--- node1 ---\nhostname             : node1\n')

    def test_device_get(self):
        # print('execute_devices')
        self.mockDS.device_get.return_value = [{'device_type': 'compute node'}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['device', 'get', 'hostname=node1'])
            self.assertEqual(output.getvalue(), '--- None ---\ndevice_type          : compute node\n')

    def test_device_get_no_match(self):
        # print('execute_devices')
        self.mockDS.device_get.return_value = []
        result = self.dscli.parse_and_run(['device', 'get', 'hostname=node1'])
        self.assertEqual(result, 1)

    def test_device_set_no_existing_device(self):
        # print('execute_devices')
        self.mockDS.device_get.return_value = []
        result = self.dscli.parse_and_run(['device', 'set', 'hostname=node1'])
        self.assertEqual(result, 0)

    def test_device_neg(self):
        # print('execute_devices')
        self.mockDS.device_get.return_value = [{'hostname': 'node1', 'device_type': 'compute node'}]
        result = self.dscli.parse_and_run(['device', 'get'])
        self.assertEqual(result, 1)

    def test_device_upsert(self):
        self.mockDS.device_get.return_value = [{'hostname': 'node1'}]
        result = self.dscli.parse_and_run(['device', 'set', 'hostname=node', 'ip_address=127.0.0.1'])
        self.assertEqual(result, 0)

    def test_device_delete(self):
        self.mockDS.device_get.return_value = [{'hostname': 'node1'}]
        result = self.dscli.parse_and_run(['device', 'delete', 'hostname=node'])
        self.assertEqual(result, 0)

    def test_device_fatal_delete(self):
        self.mockDS.device_get.return_value = [{'hostname': 'node'}]
        result = self.dscli.parse_and_run(['device', 'delete', 'hostname=node', '--fatal'])
        self.assertEqual(result, 0)

    def test_profiles(self):
        self.mockDS.profile_get.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'list'])
        self.assertEqual(result, 0)

    def test_profiles_delete(self):
        self.mockDS.profile_get.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'delete', 'profile_name=compute node'])
        self.assertEqual(result, 0)

    def test_profiles_upsert(self):
        self.mockDS.profile_get.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'set', 'profile_name=compute node'])
        self.assertEqual(result, 0)

    def test_profile_get_no_match(self):
        self.mockDS.profile_get.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'get', 'profile_name=compute node'])
        self.assertEqual(result, 0)

    def test_profile_get_no_match(self):
        self.mockDS.profile_get.return_value = []
        result = self.dscli.parse_and_run(['profile', 'get', 'profile_name=node'])
        self.assertEqual(result, 1)

    def test_profile_set_no_existing_device(self):
        # print('execute_devices')
        self.mockDS.profile_get.return_value = []
        result = self.dscli.parse_and_run(['profile', 'set', 'profile_name=node'])
        self.assertEqual(result, 0)

    def test_profile_neg(self):
        # print('execute_devices')
        self.mockDS.profile_get.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'get'])
        self.assertEqual(result, 1)

    def test_configuration_get(self):
        # print('execute_configurations')
        self.mockDS.configuration_get.return_value = [{'key': 'key1'}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['config', 'get', 'key=key1'])
            self.assertEqual(output.getvalue(), "key1 : [{'key': 'key1'}]\n")

    def test_configuration_get_no_match(self):
        # print('execute_configurations')
        self.mockDS.configuration_get.return_value = None
        result = self.dscli.parse_and_run(['config', 'get', 'key=key1'])
        self.assertEqual(result, 1)

    def test_configuration_set_no_existing_configuration(self):
        # print('execute_configurations')
        self.mockDS.configuration_get.return_value = []
        result = self.dscli.parse_and_run(['config', 'set', 'key=key1'])
        self.assertEqual(result, 1)

    def test_configuration_neg(self):
        # print('execute_configurations')
        self.mockDS.configuration_get.return_value = [{'hostname': 'node1', 'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'get'])
        self.assertEqual(result, 1)

    def test_configuration_upsert(self):
        self.mockDS.configuration_get.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'set', 'key=key4', 'value=value1'])
        self.assertEqual(result, 0)

    def test_configuration_upsert_none(self):
        self.mockDS.configuration_get.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'set'])
        self.assertEqual(result, 1)

    def test_configuration_delete(self):
        self.mockDS.configuration_get.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'delete', 'key=key1'])
        self.assertEqual(result, 0)

    def test_configuration_delete_none(self):
        self.mockDS.configuration_get.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'delete'])
        self.assertEqual(result, 1)

    def test_log_begin_end(self):
        self.mockDS.log_get_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', '--begin', '01/01/2017', '--end', '03/01/2017', 'get'])
        self.assertEqual(result, 0)

    def test_log_begin_none(self):
        self.mockDS.log_get_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', '--end', '03/01/2017', 'get'])
        self.assertEqual(result, 0)

    def test_log_begin_end_none(self):
        self.mockDS.log_get_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', '--begin', '03/01/2017', 'get'])
        self.assertEqual(result, 0)

    def test_log_end_none(self):
        self.mockDS.log_get_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', 'get'])
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
