# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolAdd Plugin.
"""
import unittest

from mock import MagicMock, patch
from ..resource_pool_check import PluginMetadata
from .. import ResourcePoolCheckCommand
from ....plugin.manager import PluginManager
from ....ctrl_logger.ctrl_logger import CtrlLogger


class TestResourcePoolCheckCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    @patch("control.ctrl_logger.ctrl_logger.CtrlLogger", spec=CtrlLogger)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.setup_mock_config()
        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.resource_manager_mock = self.mock_plugin_manager.factory_create_instance.return_value
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
        self.assertEqual('resource_pool_check', metadata.name())
        self.assertEqual(100, metadata.priority())
        self.assertIsNotNone(metadata.create_instance(self.config))

    def test_execute(self):
        self.assertEqual(self.resource_check.execute().return_code, 0)

    def test_execute_wrong_node_type(self):
        self.resource_manager_mock.check_resource_manager_installed.return_value = False

        self.assertEqual(-2, self.resource_check.execute().return_code)


if __name__ == '__main__':
    unittest.main()
