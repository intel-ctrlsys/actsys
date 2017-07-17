# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Test the OOb sensor command Plugin.
"""
import unittest
from mock import MagicMock, patch
from .. import OobSensorCommand
from ....plugin.manager import PluginManager
from datastore import DataStore


class TestOobSensorCommand(unittest.TestCase):
    """Test case for the Oob Sensor command"""

    @patch("datastore.DataStore", spec=DataStore)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.node_name = "knl-123"
        self.setup_mock_config(self.node_name)

        self.mock_plugin_manager = mock_plugin_manager
        self.oob_manager_mock = self.mock_plugin_manager.create_instance.return_value
        self.config = {
                'hostname': self.node_name,
                'configuration': self.configuration_manager,
                'plugin_manager': mock_plugin_manager,
                'logger': mock_logger,
                "bmc_fa_port": 1001,
                }
        self.config1 = {
                'hostname': self.node_name,
                'configuration': self.configuration_manager1,
                'plugin_manager': mock_plugin_manager,
                'logger': mock_logger,
                "bmc_fa_port": 1001,
                }
        self.oob_sensor_cmd = OobSensorCommand(self.node_name, **self.config)
        self.oob_sensor_cmd1 = OobSensorCommand("fake_node", **self.config1)

    def setup_mock_config(self,node_name):
        self.configuration_manager = MagicMock()
        self.configuration_manager1 = MagicMock()
        self.bmc = {
            "ip_address": "localhost",
            "rest_server_port": "5000",
            "user": "root",
            "access_type": "mock",
            "password": "password"
        }
        self.configuration_manager.get_device.return_value = {
            'device_name': self.node_name,
            "ip_address": "192.168.1.1",
            "port": 22,
            "user": "user",
            "password": "pass",
            "device_type": "node",
            "access_type": "mock",
            "bmc": self.bmc
         }
        self.configuration_manager1.get_device.return_value = None

    def test_execute_wrong_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = "xyz"
        try:
            self.oob_sensor_cmd.setup()
            self.fail('No RuntimeError raised')
        except RuntimeError:
            pass

    def test_execute_no_config_type(self):
        self.configuration_manager.get_device.return_value["access_type"] = None
        try:
            self.oob_sensor_cmd.setup()
            self.fail('No RuntimeError raised')
        except RuntimeError:
            pass


    def test_execute_all_good(self):
        try:
            self.oob_sensor_cmd.setup()
        except RuntimeError as ex:
            print(ex)
            self.fail('RuntimeError raised')


if __name__ == '__main__':
    unittest.main()
