# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Test the OOb sensor command Plugin.
"""
from .. import OobSensorGetTimeCommand
from .test_oob_sensor_command import TestOobSensorCommand


class TestOobSensorGetTimeCommand(TestOobSensorCommand):
    def setUp(self):
        super(TestOobSensorGetTimeCommand, self).setUp()
        self.oob_sensor_get_time = OobSensorGetTimeCommand(self.node_name, self.configuration_manager,
                                                           self.mock_plugin_manager, None, 'temp,ivoc_voltage', 3, 5)
        self.oob_sensor_get_time_string = OobSensorGetTimeCommand(self.node_name, self.configuration_manager,
                                                                  self.mock_plugin_manager, None, 'temp', 'p', 'l')
        self.oob_sensor_get_time_zero = OobSensorGetTimeCommand(self.node_name, self.configuration_manager,
                                                                self.mock_plugin_manager, None, 'temp', 0, 0)
        self.oob_sensor_get_time_float = OobSensorGetTimeCommand(self.node_name, self.configuration_manager,
                                                                 self.mock_plugin_manager, None, 'temp', '3.2', '1.2')

    def test_ret_msg(self):
        self.assertEqual(self.oob_sensor_get_time.execute().return_code, 0)
        self.assertEqual(self.oob_sensor_get_time_float.execute().return_code, 0)
        self.oob_manager_mock.get_sensor_value_over_time.return_value = {u'temp': [0.0, 0.88765444, 0.0, 0.0, 0.0, 0.88765444, 0.0, 0.0, 0.0, 0.88765444, 0.0, 0.0]}
        self.assertEqual(self.oob_sensor_get_time_float.execute().return_code, 0)
        self.oob_manager_mock.get_sensor_value_over_time.side_effect = RuntimeError
        self.assertEqual(self.oob_sensor_get_time.execute().return_code, 0)

    def test_error_raised(self):
        with self.assertRaises(RuntimeError):
            self.oob_sensor_get_time_zero.execute()
        with self.assertRaises(RuntimeError):
            self.oob_sensor_get_time_string.execute()
