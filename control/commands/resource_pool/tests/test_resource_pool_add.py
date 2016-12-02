# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolAdd Plugin.
"""
import unittest

from mock import MagicMock, patch

from ..resource_pool_add import PluginMetadata
from .. import ResourcePoolAddCommand
from ....plugin.manager import PluginManager
from ....ctrl_logger.ctrl_logger import CtrlLogger


class TestResourcePoolAddCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    @patch("control.ctrl_logger.ctrl_logger.CtrlLogger", spec=CtrlLogger)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.setup_mock_config()
        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.resource_manager_mock = self.mock_plugin_manager.factory_create_instance.return_value
        self.resource_manager_mock.add_node_to_resource_pool.return_value = (0, "foo")

        self.config = {
                'device_name': self.node_name,
                'configuration': self.configuration_manager,
                'plugin_manager': mock_plugin_manager,
                'logger': mock_logger,
                'arguments': None
            }
        self.resource_add = ResourcePoolAddCommand(self.config)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        obj = self.configuration_manager.get_device.return_value
        setattr(obj, "ip_address", "192.168.1.1")
        setattr(obj, "port", "22")
        setattr(obj, "user", "user")
        setattr(obj, "password", "pass")
        setattr(obj, "device_type", "node")
        setattr(obj, "service_list", [])

    def test_metadata(self):
        metadata = PluginMetadata()
        self.assertEqual('command', metadata.category())
        self.assertEqual('resource_pool_add', metadata.name())
        self.assertEqual(100, metadata.priority())
        self.assertIsNotNone(metadata.create_instance(self.config))

    def test_execute(self):
        self.assertEqual(self.resource_add.execute().return_code, 0)

    def test_execute_wrong_node_type(self):
        self.configuration_manager.get_device.return_value.device_type = "Problems"

        self.assertEqual(-1, self.resource_add.execute().return_code)

if __name__ == '__main__':
    unittest.main()
