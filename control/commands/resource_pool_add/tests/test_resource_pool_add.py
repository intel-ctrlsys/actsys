# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolAdd Plugin.
"""
import unittest
from mock import MagicMock, patch
from ..resource_pool_add import ResourcePoolAddCommand
from ..resource_pool_add import PluginMetadata
from ....plugin.manager import PluginManager
from ....resource.slurm.slurm_resource_control import SlurmResource


class TestResourcePoolAddCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    def setUp(self):
        self.setup_mock_config()
        self.node_name = "knl-123"
        self.config = {
                'device_name': self.node_name,
                'configuration': self.configuration_manager,
                'plugin_manager': PluginManager(),
                'logger': None,
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

    @patch.object(SlurmResource, "add_node_to_resource_pool")
    def test_execute(self, mock_sr):
        mock_sr.return_value = (0, "foo")
        self.assertEqual(self.resource_add.execute().return_code, 0)


if __name__ == '__main__':
    unittest.main()
