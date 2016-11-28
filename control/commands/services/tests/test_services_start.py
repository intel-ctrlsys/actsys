# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ServicesCheckCommand Plugin.
"""
import unittest
from mock import patch, MagicMock

from .. import ServicesStartCommand
from .. import ServicesStartPluginMetadata as PluginMetadata
from ....plugin.manager import PluginManager


class TestServicesStartCommand(unittest.TestCase):
    """Test case for the ServicesCheckCommand class."""

    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager):
        self.setup_mock_config()

        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.ssh_mock = self.mock_plugin_manager.factory_create_instance.return_value
        self.ssh_mock.execute.return_value = [0, None]

        self.configuration = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': self.mock_plugin_manager,
            'logger': None,
            'arguments': None
        }
        self.services_check = ServicesStartCommand(self.configuration)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        obj = self.configuration_manager.get_device.return_value
        setattr(obj, "ip_address", "192.168.1.1")
        setattr(obj, "port", "22")
        setattr(obj, "user", "user")
        setattr(obj, "password", "pass")
        setattr(obj, "device_type", "compute")
        setattr(obj, "service_list", [])

    def test_metadata(self):
        metadata = PluginMetadata()
        self.assertEqual('command', metadata.category())
        self.assertEqual('service_start', metadata.name())
        self.assertEqual(100, metadata.priority())
        self.assertIsNotNone(metadata.create_instance(self.configuration))


if __name__ == '__main__':
    unittest.main()
