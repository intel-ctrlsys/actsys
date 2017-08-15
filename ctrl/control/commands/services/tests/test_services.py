# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Test the ServicesCheckCommand Plugin.
"""
import unittest
from mock import patch, MagicMock
from datastore import DataStoreLogger
from ..services_status import ServicesStatusCommand
from ....plugin.manager import PluginManager
from ....utilities import SubprocessOutput


class TestServicesCommand(unittest.TestCase):
    """Test case for the ServicesCheckCommand class."""

    @patch("datastore.DataStoreLogger", spec=DataStoreLogger)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):

        self.node_name = "knl-123"
        self.setup_mock_config()
        self.mock_plugin_manager = mock_plugin_manager
        self.ssh_mock = self.mock_plugin_manager.create_instance.return_value
        self.ssh_mock.execute_multiple_nodes.return_value = {"192.168.1.1": SubprocessOutput(0, None, None)}

        self.configuration = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': self.mock_plugin_manager,
            'logger': mock_logger
        }
        self.services = ServicesStatusCommand(**self.configuration)
        self.services.command = ["systemctl", "status"]

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        self.configuration_manager.get_device.return_value = {
            "ip_address": "192.168.1.1",
            "port": 22,
            "hostname": self.node_name,
            "user": "user",
            "password": "pass",
            "device_type": "node",
            "service_list": ['orcmd']
        }

    def test_empty_services(self):
        """Stub test, please update me"""
        self.configuration_manager.get_device.return_value = {
            "ip_address": "192.168.1.1",
            "port": 22,
            "hostname": self.node_name,
            "user": "user",
            "password": "pass",
            "device_type": "node",
            "service_list": []
        }
        self.assertEqual(self.services.execute()[0].message, 'Success: no services checked')

    def test_services_success(self):
        """Stub test, please update me"""
        self.ssh_mock.execute_multiple_nodes.return_value = \
            {"192.168.1.1": SubprocessOutput(0, "0 - {}: Success: status - orcmd".format(self.node_name), None)}
        self.assertEqual(self.services.execute()[0].message, "0 - 0 - {}: Success: status - orcmd - None"
                         .format(self.node_name))
        self.assertTrue(self.mock_plugin_manager.create_instance.called)

    def test_services_exception(self):
        """Failing, failing all the day"""
        self.ssh_mock.execute_multiple_nodes.side_effect = RuntimeError
        self.services.execute()

    def test_services_unable_to_connect(self):
        self.ssh_mock.execute.return_value = SubprocessOutput(255, None, None)

        self.assertEqual(self.services.execute()[0].message,
                         "0 - None - None")

if __name__ == '__main__':
    unittest.main()
