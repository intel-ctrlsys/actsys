# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ServicesCheckCommand Plugin.
"""
import unittest
from mock import patch, MagicMock

from .. import ServicesStopCommand
from ....plugin.manager import PluginManager


class TestServicesStopCommand(unittest.TestCase):
    """Test case for the ServicesCheckCommand class."""

    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager):
        self.setup_mock_config()

        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.ssh_mock = self.mock_plugin_manager.create_instance.return_value
        self.ssh_mock.execute.return_value = [0, None]

        self.configuration = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': self.mock_plugin_manager,
            'logger': None,
            'arguments': None
        }
        self.services_check = ServicesStopCommand(self.configuration)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        obj = self.configuration_manager.get_device.return_value
        setattr(obj, "ip_address", "192.168.1.1")
        setattr(obj, "port", "22")
        setattr(obj, "user", "user")
        setattr(obj, "password", "pass")
        setattr(obj, "device_type", "compute")
        setattr(obj, "service_list", [])


if __name__ == '__main__':
    unittest.main()
