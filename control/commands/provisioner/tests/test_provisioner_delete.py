# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the ProvisionerDelete Plugin.
"""
import unittest
from mock import patch, MagicMock
from datastore import DataStoreLogger
from ..provisioner_delete import ProvisionerDeleteCommand
from ....plugin.manager import PluginManager


class TestProvisionerDeleteCommand(unittest.TestCase):
    """Test the ProvisionerDelete Plugin."""

    @patch("datastore.DataStoreLogger", spec=DataStoreLogger)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.setup_mock_config()

        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.provisioner_mock = self.mock_plugin_manager.create_instance.return_value

        self.configuration = {
            'device_name': self.node_name,
            'configuration': self.configuration_manager,
            'plugin_manager': self.mock_plugin_manager,
            'logger': mock_logger,
            'arguments': None
        }
        self.prov_delete = ProvisionerDeleteCommand(self.configuration)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        self.configuration_manager.get_device.return_value = {
            "device_type": "node",
            "provisioner": "mock",
            "device_id": 1
        }

    def test_no_provisioner_in_config(self):
        self.configuration_manager.get_device.return_value.pop("provisioner")
        with self.assertRaises(RuntimeError):
            ProvisionerDeleteCommand(self.configuration)

    def test_incorrect_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = 'Not Compute'

        result = self.prov_delete.execute()

        self.assertEqual(result.return_code, 1, "Expected error code")
        self.assertEqual(result.message,
                         'Failure: cannot perform provisioner actions on this device type ({})'.format('Not Compute'))

    def test_success(self):
        result = self.prov_delete.execute()

        self.assertEqual(0, result.return_code)
        self.assertEqual("Successfully deleted {} from the provisioner".format(1), result.message)