# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Test the diag command Plugin.
"""
import unittest
from mock import MagicMock, patch
from .. import DiagnosticsCommand
from ....plugin.manager import PluginManager
from datastore import DataStore


class TestDiagnosticsCommand(unittest.TestCase):
    """Test case for the diagnostics inband command"""

    @patch("datastore.DataStore", spec=DataStore)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.node_name = "knl-123"
        self.setup_mock_config(self.node_name)

        self.mock_plugin_manager = mock_plugin_manager
        self.diag_manager_mock = self.mock_plugin_manager.create_instance.return_value
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
        self.diag_cmd = DiagnosticsCommand(self.node_name, **self.config)
        self.diag_cmd1 = DiagnosticsCommand("fake_node", **self.config1)

    def setup_mock_config(self, node_name):
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
            'device_name': node_name,
            "ip_address": "192.168.1.1",
            "diagnostics": "inband_diagnostics",
            "port": 22,
            "user": "user",
            "password": "pass",
            "device_type": "node",
            "bmc": self.bmc
         }
        self.configuration_manager1.get_device.return_value = None

    def test_execute_wrong_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = "xyz"
        try:
            self.diag_cmd.setup()
            self.fail('No RuntimeError raised')
        except RuntimeError:
            pass

    def test_execute_all_good(self):
        try:
            self.diag_cmd.setup()
        except RuntimeError:
            self.fail('RuntimeError raised')


if __name__ == '__main__':
    unittest.main()
