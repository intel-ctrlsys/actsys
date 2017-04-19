# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the mock oob sensor plugin.
"""
import unittest
from ..oob_sensor_mock import OobSensorMock
from ...oob_sensors import OobSensor


class TestOobSensorMock(unittest.TestCase):
    """Test the oob sensor mock plugin."""

    def test_oob_sensor(self):
        node1 = OobSensor('test_node1')
        node1.get_sensor_value_over_time('none', 'none', 'none', None, None)
        node1.get_sensor_value('name', None, None)

    def test_mock_oob_sensor(self):
        node1 = OobSensorMock('test_node1')
        try:
            node1.get_sensor_value("voltage", None, None)
            pass
        except RuntimeError:
            self.fail('Exception raised')

    def test_mock_oob_sensor_all(self):
        node1 = OobSensorMock({'device_name': 'test_node_1', 'device_type': 'node'})
        self.assertEqual("All sensor value(s) is 10", node1.get_sensor_value(".*", None, None))

    def test_mock_over_time(self):
        node1 = OobSensorMock({'device_name': 'test_node_1', 'device_type': 'node'})
        try:
            node1.get_sensor_value_over_time('voltage', 3, 2, None, None)
            pass
        except RuntimeError:
            self.fail('Exception raised')

    def test_mock_oob_sensor_time_all(self):
        node1 = OobSensorMock({'device_name': 'test_node_1', 'device_type': 'node'})
        try:
            node1.get_sensor_value(".*", None, None)
            pass
        except RuntimeError:
            self.fail('Exception raised')
