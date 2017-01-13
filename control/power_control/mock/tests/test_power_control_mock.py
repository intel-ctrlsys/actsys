# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the mock power control object.
"""
import unittest
import os
from ..power_control_mock import PowerControlMock


class TestPowerControlMock(unittest.TestCase):
    """Test the power control mock test."""
    def setUp(self):
        self.mock1 = PowerControlMock({'device_name': 'test_node_1',
                                       'device_type': 'node'})
        self.mock2 = PowerControlMock({'device_name': 'test_node_2',
                                       'device_type': 'node'})
        self.mock2.set_device_power_state('On:bmc_on')

    def tearDown(self):
        if os.path.exists(self.mock1.file_path):
            os.unlink(self.mock1.file_path)
        if os.path.exists(self.mock2.file_path):
            os.unlink(self.mock2.file_path)

    def test_mock_power_control(self):
        node1 = PowerControlMock({'device_name': 'test_node_1',
                                  'device_type': 'node'})
        node2 = PowerControlMock({'device_name': 'test_node_2',
                                  'device_type': 'node'})
        self.assertEqual('Off', node1.get_current_device_power_state())
        self.assertEqual('On:bmc_on', node2.get_current_device_power_state())

        node1.set_device_power_state('On')
        self.assertEqual('On:bmc_on', node1.get_current_device_power_state())

        node1.set_device_power_state('Off')
        self.assertEqual('Off', node1.get_current_device_power_state())

        node2.set_device_power_state('On:efi')
        self.assertEqual('On', node2.get_current_device_power_state())

    def test_bad_type(self):
        with self.assertRaises(RuntimeError):
            PowerControlMock({'device_name': 'test_node_1',
                              'device_type': 'network_switch'})

    def test_bad_target(self):
        node = PowerControlMock({'device_name': 'test_node_1',
                                 'device_type': 'node'})
        with self.assertRaises(RuntimeError):
            node.set_device_power_state('Sleep')
        with self.assertRaises(RuntimeError):
            node.set_device_power_state('On:full')
        with self.assertRaises(RuntimeError):
            node.set_device_power_state('Off:full')
