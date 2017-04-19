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

    def test_ret_msg(self):
        self.assertEqual(self.oob_sensor_get.execute().return_code, 0)
        self.oob_manager_mock.get_sensor_value.side_effect = RuntimeError
        self.assertEqual(self.oob_sensor_get.execute().return_code, 1)
