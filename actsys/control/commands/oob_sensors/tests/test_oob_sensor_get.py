# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Test the OOb sensor command Plugin.
"""
from .. import OobSensorGetCommand
from .test_oob_sensor_command import TestOobSensorCommand


class TestOobSensorGetCommand(TestOobSensorCommand):
    def setUp(self):
        super(TestOobSensorGetCommand, self).setUp()
        self.oob_sensor_get = OobSensorGetCommand(self.node_name, self.configuration_manager,
                                                  self.mock_plugin_manager, None, 'temp')
        self.oob_sensor_get_empty = OobSensorGetCommand(self.node_name, self.configuration_manager,
                                                        self.mock_plugin_manager, None, '')
        self.oob_sensor_get_all = OobSensorGetCommand(self.node_name, self.configuration_manager,
                                                      self.mock_plugin_manager, None, 'all')
        self.oob_sensor_get1 = OobSensorGetCommand(self.node_name, self.configuration_manager,
                                                   self.mock_plugin_manager, None, 'temp,ivoc_voltage')

    def test_ret_msg(self):
        try:
            self.oob_sensor_get_empty.execute()
            self.fail("no error")
        except RuntimeError:
            pass
        self.assertEqual(self.oob_sensor_get_all.execute()[0].return_code, 0)
        self.assertEqual(self.oob_sensor_get1.execute()[0].return_code, 0)
        self.assertEqual(self.oob_sensor_get.execute()[0].return_code, 0)
        self.oob_manager_mock.get_sensor_value.return_value = {"node": {'temp': [0.88765444]}}
        self.assertEqual(self.oob_sensor_get.execute()[0].return_code, 0)
        self.oob_manager_mock.get_sensor_value.side_effect = RuntimeError
        self.assertEqual(self.oob_sensor_get.execute()[0].return_code, 255)
