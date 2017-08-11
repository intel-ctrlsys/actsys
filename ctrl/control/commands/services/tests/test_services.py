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
from ..services import ServicesCommand
from ....plugin.manager import PluginManager
from ....utilities import SubprocessOutput

class TestServicesCommand(unittest.TestCase):
    """Test case for the ServicesCheckCommand class."""

    @patch("datastore.DataStoreLogger", spec=DataStoreLogger)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.setup_mock_config()

        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.ssh_mock = self.mock_plugin_manager.create_instance.return_value
        self.ssh_mock.execute.return_value = SubprocessOutput(0, None, None)

        self.configuration = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': self.mock_plugin_manager,
            'logger': mock_logger
        }
        self.services = ServicesCommand(**self.configuration)
        self.services.command = ["systemctl", "status"]

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

    def test_incorrect_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = 'Not Compute'

        result = self.services.execute()

        self.assertEqual(result.return_code, 1, "Expected error code")
        self.assertEqual(result.message,
                         'Failure: cannot perform service actions this device type ({})'.format('Not Compute'))

    def test_empty_services(self):
        """Stub test, please update me"""
        self.assertEqual(self.services.execute().message, 'Success: no services checked')

    def test_services_success(self):
        """Stub test, please update me"""
        self.services.device["service_list"] = ['orcmd']
        self.assertEqual(self.services.execute().message, "0 - Success: status - orcmd")

        self.assertTrue(self.mock_plugin_manager.create_instance.called)
        self.ssh_mock.execute.assert_called_with(
            ['systemctl', 'status', 'orcmd'],
            self.services.remote_access_data,
            True
        )

    def test_services_failure(self):
        """Failing, failing all the day"""
        self.services.device["service_list"] = ['orcmd']
        self.ssh_mock.execute.return_value = SubprocessOutput(1, None, None)

        self.assertEqual(self.services.execute().message, "1 - Failed: status - orcmd")

        self.ssh_mock.execute.return_value = SubprocessOutput(1, "Such a service does not exist", None)
        self.assertEqual(self.services.execute().message, "1 - Failed: status - orcmd\n Such a service does not exist")

    def test_services_unable_to_connect(self):
        self.ssh_mock.execute.return_value = SubprocessOutput(255, None, None)
        self.services.device["service_list"] = ['orcmd']

        self.assertEqual(self.services.execute().message,
                         "255 - Failed: status - orcmd")

if __name__ == '__main__':
    unittest.main()