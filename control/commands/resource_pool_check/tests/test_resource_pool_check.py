# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ResourcePoolCheck Plugin.
"""
import unittest
from ..resource_pool_check import ResourcePoolCheckCommand
from ..resource_pool_check import PluginMetadata
from ....plugin.manager import PluginManager


class TestResourcePoolCheckCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    def setUp(self):
        self.node_name = "knl-123"
        self.resource_check = ResourcePoolCheckCommand(
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
        self.assertEqual('resource_pool_check', metadata.name())
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
        self.assertEqual(self.resource_check.execute().return_code, 0)


if __name__ == '__main__':
    unittest.main()
