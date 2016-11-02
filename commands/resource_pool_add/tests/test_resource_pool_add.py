# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolAdd Plugin.
"""
import unittest
from ctrl.commands.resource_pool_add import ResourcePoolAddCommand
from ctrl.commands.resource_pool_add import PluginMetadata
from ctrl.plugin.manager import PluginManager


class TestResourcePoolAddCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    def setUp(self):
        self.node_name = "knl-123"
        self.resource_add = ResourcePoolAddCommand(
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
        self.assertEqual('resource_pool_add', metadata.name())
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
        """Stub test, please update me"""

        self.assertEqual(self.resource_add.execute().message,
                         "Success: Resource Pool Add {}".format(self.node_name))


if __name__ == '__main__':
    unittest.main()
