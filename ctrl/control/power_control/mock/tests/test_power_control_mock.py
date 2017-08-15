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
        self.mock1 = PowerControlMock(device_list=[{
                'device_id': 'test_node_1',
                'hostname': 'test_node_1',
                'device_type': 'node',
                'access_type': 'mock',
                'bmc': 'test_bmc'
            }])
        self.mock2 = PowerControlMock(device_list=[{
                'device_id': 'test_node_2',
                'hostname': 'test_node_2',
                'device_type': 'node',
                'access_type': 'mock',
                'bmc': 'test_bmc'
            }])
        self.mock2.set_device_power_state('On:bmc_on')

    def tearDown(self):
        node_list = ['test_node_1', 'test_node_2']
        for node in node_list:
            filename = node + "." + 'state'
            file_path = os.path.join(os.path.sep, 'tmp', filename)
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_mock_power_control(self):
        node1 = PowerControlMock(device_list=[{
                'device_id': 'test_node_1',
                'hostname': 'test_node_1',
                'device_type': 'node',
                'access_type': 'mock',
                'bmc': 'test_bmc'
            }])
        node2 = PowerControlMock(device_list=[{
                'device_id': 'test_node_2',
                'hostname': 'test_node_2',
                'device_type': 'node',
                'access_type': 'mock',
                'bmc': 'test_bmc'
            }])
        self.assertEqual('Off', node1.get_current_device_power_state()['test_node_1'])
        self.assertEqual('On:bmc_on', node2.get_current_device_power_state()['test_node_2'])

        node1.set_device_power_state('On')
        self.assertEqual('On:bmc_on', node1.get_current_device_power_state()['test_node_1'])

        node1.set_device_power_state('Off')
        self.assertEqual('Off', node1.get_current_device_power_state()['test_node_1'])

        node2.set_device_power_state('On:efi')
        self.assertEqual('On', node2.get_current_device_power_state()['test_node_2'])

    def test_bad_target(self):
        node = PowerControlMock(device_list=[{
                'device_id': 'test_node_1',
                'hostname': 'test_node_1',
                'device_type': 'node',
                'access_type': 'mock',
                'bmc': 'test_bmc'
            }])
        with self.assertRaises(RuntimeError):
            node.set_device_power_state('Sleep')
        with self.assertRaises(RuntimeError):
            node.set_device_power_state('On:full')
        with self.assertRaises(RuntimeError):
            node.set_device_power_state('Off:full')
