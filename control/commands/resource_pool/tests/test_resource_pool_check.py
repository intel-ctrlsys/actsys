# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolAdd Plugin.
"""
import unittest

from mock import MagicMock, patch
from .. import ResourcePoolCheckCommand
from ....plugin.manager import PluginManager
from ....datastore import DataStore


class TestResourcePoolCheckCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    @patch("control.datastore.DataStore", spec=DataStore)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.setup_mock_config()
        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.resource_manager_mock = self.mock_plugin_manager.create_instance.return_value
        self.resource_manager_mock.check_node_state.return_value = (0, "foo")

        self.config = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': mock_plugin_manager,
            'logger': mock_logger,
            'arguments': None
        }
        self.resource_check = ResourcePoolCheckCommand(self.config)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        self.configuration_manager.get_device.return_value = {
            "ip_address": "192.168.1.1",
            "port": 22,
            "user": "user",
            "password": "pass",
            "device_type": "node",
            "service_list": []
        }

    def test_execute(self):
        self.assertEqual(self.resource_check.execute().return_code, 0)

    def test_execute_wrong_node_type(self):
        self.resource_manager_mock.check_resource_manager_installed.return_value = False

        self.assertEqual(-2, self.resource_check.execute().return_code)


if __name__ == '__main__':
    unittest.main()
