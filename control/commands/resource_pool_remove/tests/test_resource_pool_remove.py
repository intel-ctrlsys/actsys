# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolRemove Plugin.
"""
import unittest
from ..resource_pool_remove import ResourcePoolRemoveCommand
from ..resource_pool_remove import PluginMetadata
from ....plugin.manager import PluginManager


class TestResourcePoolRemoveCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    def setUp(self):
        self.node_name = "knl-123"
        self.resource_remove = ResourcePoolRemoveCommand(
            {
                'device_name': self.node_name,
                'configuration': [],
                'plugin_manager': PluginManager(),
                'logger': None,
                'arguments': None
            })

    def test_metadata(self):
        metadata = PluginMetadata()
        self.assertEqual('command', metadata.category())
        self.assertEqual('resource_pool_remove', metadata.name())
        self.assertEqual(100, metadata.priority())
        self.assertIsNotNone(metadata.create_instance(
            {
                'device_name': self.node_name,
                'configuration': [],
                'plugin_manager': PluginManager(),
                'logger': None,
                'arguments': None
            }))

    def test_execute(self):
        self.assertEqual(self.resource_remove.execute().return_code,
                         0)


if __name__ == '__main__':
    unittest.main()
