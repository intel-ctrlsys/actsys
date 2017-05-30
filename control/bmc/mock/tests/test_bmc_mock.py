# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the Mock plugin for BMC access/control.
"""
import os
import unittest
import tempfile
from ..bmc import BmcMock
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData


class TestBmcMock(unittest.TestCase):
    def setUp(self):
        self.bmc_file = os.path.join(os.path.sep, 'tmp', 'bmc_file')
        self.remote = RemoteAccessData('127.0.0.2', 0, 'admin', 'root')
        self.bios_file = os.path.sep + os.path.join(tempfile.gettempdir(), 'bios_file')
        self.device = {'device_name': 'localhost'}
        self.bmc = None

    def test_metadata_mock(self):
        manager = PluginManager()
        manager.register_plugin_class(BmcMock)
        bmc = manager.create_instance('bmc', 'mock')
        self.assertIsNotNone(bmc)

    def test_persist_state(self):
        if os.path.exists(self.bmc_file):
            os.unlink(self.bmc_file)
        bmc = BmcMock()
        self.assertEqual(5, bmc.state_change_delay)
        self.assertFalse(bmc.get_chassis_state(self.remote))
        bmc.set_chassis_state(self.remote, 'on')
        with self.assertRaises(RuntimeError):
            bmc.set_chassis_state(self.remote, 'crazy')
        self.assertTrue(bmc.get_chassis_state(self.remote))

        bmc = BmcMock()
        self.assertTrue(bmc.get_chassis_state(self.remote))

    def test_persist_state_1(self):
        if os.path.exists(self.bios_file):
            os.unlink(self.bios_file)
        mock_bmc = BmcMock()
        self.assertTrue('No image found' in mock_bmc.get_version(self.device, self.bmc))
        self.assertTrue('Bios for' in mock_bmc.bios_update(self.device, self.bmc, 'test.bin'))
        self.assertTrue('test.bin' in mock_bmc.get_version(self.device, self.bmc))

        mock_bmc = BmcMock()
        self.assertTrue(mock_bmc.get_version(self.device, self.bmc))

    def test_mock_oob_sensor(self):
        node1 = BmcMock()
        try:
            node1.get_sensor_value("voltage", None, None)
            pass
        except RuntimeError:
            self.fail('Exception raised')

    def test_mock_oob_sensor_all(self):
        node1 = BmcMock()
        self.assertEqual({'All sensors': [10]}, node1.get_sensor_value(".*", None, None))

    def test_mock_over_time(self):
        node1 = BmcMock()
        try:
            node1.get_sensor_value_over_time('voltage', 3, 2, None, None)
            pass
        except RuntimeError:
            self.fail('Exception raised')

    def test_mock_oob_sensor_time_all(self):
        node1 = BmcMock()
        try:
            node1.get_sensor_value(".*", None, None)
            pass
        except RuntimeError:
            self.fail('Exception raised')
