# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolAdd Plugin.
"""
import unittest

from mock import MagicMock, patch

from .. import ResourcePoolAddCommand
from ....plugin.manager import PluginManager
from datastore import DataStore


class TestResourcePoolAddCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    @patch("datastore.DataStore", spec=DataStore)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.node_name = "knl-123"
        self.setup_mock_config()
        self.mock_plugin_manager = mock_plugin_manager
        self.resource_manager_mock = self.mock_plugin_manager.create_instance.return_value
        self.resource_manager_mock.add_nodes_to_resource_pool.return_value = (0, "foo")

        self.config = {
                'device_name': self.node_name,
                'configuration': self.configuration_manager,
                'plugin_manager': mock_plugin_manager,
                'logger': mock_logger
            }
        self.resource_add = ResourcePoolAddCommand(**self.config)

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
        self.configuration_manager.expand_device_list.return_value = \
            [self.node_name]

    def test_execute(self):
        self.assertEqual(self.resource_add.execute().return_code, 0)

    def test_execute_wrong_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = "Problems"

        self.assertEqual(-1, self.resource_add.execute().return_code)

if __name__ == '__main__':
    unittest.main()
