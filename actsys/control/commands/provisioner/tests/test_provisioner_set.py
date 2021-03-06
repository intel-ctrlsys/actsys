# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the ProvisionerSet Plugin.
"""
import unittest
from mock import patch, MagicMock
from argparse import Namespace
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
            "device_id": 1,
            "hostname": "c1"
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
            'logger': mock_logger
        }
        self.prov_set = ProvisionerSetCommand(**self.args)

    def test_no_provisioner_in_config(self):
        self.configuration_manager.get_device.return_value.pop("provisioner")
        with self.assertRaises(RuntimeError):
            ProvisionerSetCommand(**self.args)

    def test_incorrect_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = 'Not Compute'

        result = self.prov_set.execute()

        self.assertEqual(result.return_code, 1, "Expected error code")
        self.assertEqual(result.message,
                         'Failure: cannot perform provisioner actions on this device type ({})'.format('Not Compute'))

    def test_success(self):
        result = self.prov_set.execute()

        self.assertEqual(0, result.return_code)
        self.assertEqual("Successfully set c1 options for the provisioner", result.message)

    def test_ipaddr(self):
        self.prov_set.ip_address = "foo"
        result = self.prov_set.execute()
        self.provisioner_mock.set_ip_address.assert_called_once_with(self.mock_device, "foo")

        self.prov_set.ip_address = "bar"
        self.prov_set.net_interface = "io"
        result = self.prov_set.execute()
        self.provisioner_mock.set_ip_address.assert_called_with(self.mock_device, "bar", "io")

    def test_hwaddr(self):
        self.prov_set.hw_address = "foo"
        result = self.prov_set.execute()
        self.provisioner_mock.set_hardware_address.assert_called_once_with(self.mock_device, "foo")

        self.prov_set.hw_address = "bar"
        self.prov_set.net_interface = "io"
        result = self.prov_set.execute()
        self.provisioner_mock.set_hardware_address.assert_called_with(self.mock_device, "bar", "io")

    def test_image(self):
        self.prov_set.image = "foo"

        result = self.prov_set.execute()
        self.provisioner_mock.set_image.assert_called_once_with(self.mock_device, "foo")

    def test_bootstrap(self):
        self.prov_set.bootstrap = "foo"

        result = self.prov_set.execute()
        self.provisioner_mock.set_bootstrap.assert_called_once_with(self.mock_device, "foo")

    def test_files(self):
        self.prov_set.files = "foo"

        result = self.prov_set.execute()
        self.provisioner_mock.set_files.assert_called_once_with(self.mock_device, "foo")

    def test_kargs(self):
        self.prov_set.kernel_args = "foo"

        result = self.prov_set.execute()
        self.provisioner_mock.set_kernel_args.assert_called_once_with(self.mock_device, "foo")

    def create_namespace(self, **kwargs):
        necessary_keys = ["ip_address", "net_interface", "hw_address", "image", "bootstrap", "files", "kernel_args"]
        for key in necessary_keys:
            if key not in kwargs:
                kwargs[key] = None
        return Namespace(**kwargs)
