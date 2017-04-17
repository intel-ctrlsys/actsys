# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the ProvisionerAdd Plugin.
"""
import unittest
from mock import patch, MagicMock
from datastore import DataStoreLogger
from ..provisioner_add import ProvisionerAddCommand
from ....plugin.manager import PluginManager
from argparse import Namespace

class TestProvisionerAddCommand(unittest.TestCase):
    """Test case for the ProvisionerAdd class."""

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
            'arguments': Namespace(provisioner=None)
        }
        self.prov_add = ProvisionerAddCommand(self.configuration)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        self.configuration_manager.get_device.return_value = {
            "device_type": "node",
            "provisioner": "mock",
            "device_id": 1,
            "hostname": "c1"
        }

    def test_no_provisioner_in_config(self):
        self.configuration_manager.get_device.return_value.pop("provisioner")
        with self.assertRaises(RuntimeError):
            ProvisionerAddCommand(self.configuration)

    def test_incorrect_node_type(self):
        self.configuration_manager.get_device.return_value["device_type"] = 'Not Compute'

        result = self.prov_add.execute()

        self.assertEqual(result.return_code, 1, "Expected error code")
        self.assertEqual(result.message,
                         'Failure: cannot perform provisioner actions on this device type ({})'.format('Not Compute'))

    def test_success(self):
        result = self.prov_add.execute()

        self.assertEqual(0, result.return_code)
        self.assertEqual("Successfully added c1 to the provisioner", result.message)