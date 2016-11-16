# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ServicesCheckCommand Plugin.
"""
import unittest
from mock import patch, MagicMock

from ctrl.commands.services import ServicesCheckCommand
from ctrl.commands.services import PluginMetadata
from ctrl.plugin.manager import PluginManager


class TestServicesCheckCommand(unittest.TestCase):
    """Test case for the ServicesCheckCommand class."""

    @patch("plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager):
        self.setup_mock_config()

        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.ssh_mock = self.mock_plugin_manager.factory_create_instance.return_value
        self.ssh_mock.execute.return_value.code = 0

        self.configuration = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': self.mock_plugin_manager,
            'logger': None,
            'arguments': None
        }
        self.services_check = ServicesCheckCommand(self.configuration)

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
        self.assertEqual('service_check', metadata.name())
        self.assertEqual(100, metadata.priority())
        self.assertIsNotNone(metadata.create_instance(self.configuration))

    def test_incorrect_node_type(self):
        self.configuration_manager.get_device.\
            return_value.device_type = 'Not Compute'

        result = self.services_check.execute()

        self.assertEqual(result.return_code, 1, "Expected error code")
        self.assertEqual(result.message, 'Failure: cannot check services this '
                                         'device type {}'.format('Not Compute'))

    def test_empty_services(self):
        """Stub test, please update me"""
        fmt = "Success: All services running for {}"
        self.assertEqual(self.services_check.execute().message,
                         fmt.format(self.node_name))

    def test_services_success(self):
        """Stub test, please update me"""
        self.configuration_manager.get_device.return_value.service_list = [
            'orcmd']
        fmt = "Success: All services running for {}"
        self.assertEqual(self.services_check.execute().message,
                         fmt.format(self.node_name))

        self.assertTrue(self.mock_plugin_manager.factory_create_instance.called)
        self.ssh_mock.execute.assert_called_with(
            'systemctrl status {}'.format("orcmd"),
            self.services_check.remoteAccessData
        )

    def test_services_failure(self):
        """Failing, failing all the day"""
        self.configuration_manager.get_device.return_value.service_list = [
            'orcmd']
        self.ssh_mock.execute.return_value.code = 1

        self.assertEqual(
            self.services_check.execute().message,
            "1 - Failed: orcmd service was not active.")


if __name__ == '__main__':
    unittest.main()
