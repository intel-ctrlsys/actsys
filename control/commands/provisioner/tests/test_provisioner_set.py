# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the ProvisionerSet Plugin.
"""
import unittest
from mock import patch, MagicMock
from datastore import DataStoreLogger
from ..provisioner_set import ProvisionerSetCommand
from ....plugin.manager import PluginManager


class TestProvisionerSetCommand(unittest.TestCase):
    """Test case for the ProvisionerSet class."""

    @patch("datastore.DataStoreLogger", spec=DataStoreLogger)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.mock_device = {
            "device_type": "node",
            "provisioner": "mock",
            "device_id": 1
        }
        self.configuration_manager = MagicMock()
        self.configuration_manager.get_device.return_value = self.mock_device

        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.provisioner_mock = self.mock_plugin_manager.create_instance.return_value

        self.args = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': self.mock_plugin_manager,
            'logger': mock_logger,
            'arguments': None
        }
        self.prov_set = ProvisionerSetCommand(self.args)

    def test_no_provisioner_in_config(self):
        self.configuration_manager.get_device.return_value.pop("provisioner")
        with self.assertRaises(RuntimeError):
            ProvisionerSetCommand(self.args)

    def test_incorrect_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = 'Not Compute'

        result = self.prov_set.execute()

        self.assertEqual(result.return_code, 1, "Expected error code")
        self.assertEqual(result.message,
                         'Failure: cannot perform provisioner actions on this device type ({})'.format('Not Compute'))

    def test_success(self):
        result = self.prov_set.execute()

        self.assertEqual(0, result.return_code)
        self.assertEqual("Successfully set {} to the provisioner".format(1), result.message)

    def test_ipaddr(self):
        self.prov_set.command_args = {"ip_address": "foo"}
        result = self.prov_set.execute()
        self.provisioner_mock.set_network_interface.assert_called_once_with(self.mock_device, "foo")

        self.prov_set.command_args = {"ip_address": "bar", "net_interface": "io"}
        result = self.prov_set.execute()
        self.provisioner_mock.set_network_interface.assert_called_with(self.mock_device, "bar", "io")

    def test_hwaddr(self):
        self.prov_set.command_args = {"hw_address": "foo"}
        result = self.prov_set.execute()
        self.provisioner_mock.set_hardware_address.assert_called_once_with(self.mock_device, "foo")

        self.prov_set.command_args = {"hw_address": "bar", "net_interface": "io"}
        result = self.prov_set.execute()
        self.provisioner_mock.set_hardware_address.assert_called_with(self.mock_device, "bar", "io")

    def test_image(self):
        self.prov_set.command_args = {"image": "foo"}

        result = self.prov_set.execute()
        self.provisioner_mock.set_image.assert_called_once_with(self.mock_device, "foo")

    def test_bootstrap(self):
        self.prov_set.command_args = {"bootstrap": "foo"}

        result = self.prov_set.execute()
        self.provisioner_mock.set_bootstrap.assert_called_once_with(self.mock_device, "foo")

    def test_files(self):
        self.prov_set.command_args = {"files": "foo"}

        result = self.prov_set.execute()
        self.provisioner_mock.set_files.assert_called_once_with(self.mock_device, "foo")

    def test_kargs(self):
        self.prov_set.command_args = {"kernel_args": "foo"}

        result = self.prov_set.execute()
        self.provisioner_mock.set_kernel_args.assert_called_once_with(self.mock_device, "foo")
