# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for Mockdiag plugin
"""
import unittest
from mock import MagicMock, Mock, patch
from control.diagnostics.mock_diagnostics.mock_diagnostics import MockDiagnostics
from control.console_log.mock_console_log.ipmi_mock import MockConsoleLog
from control.plugin.manager import PluginManager
from control.provisioner.provisioner import Provisioner
from control.resource.resource_control import ResourceControl
from control.power_control.power_control import PowerControl


class TestsMockDiagnostics(unittest.TestCase):
    """Unit tests for Mock Diagnostics"""

    def setUp(self):
        """Setup for tests"""
        self.setup_mock_config()
        self.mock_resource_control = Mock(spec=ResourceControl)
        self.mock_provisioner = Mock(spec=Provisioner)
        self.mock_power_control = Mock(spec=PowerControl)
        self.mock_plugin_manager = Mock(spec=PluginManager)

    def reset_for_test(self):
        """reseting all the mock return values for tests"""
        self.mock_resource_control.check_nodes_state.return_value = 0, "idle"
        self.mock_resource_control.remove_nodes_from_resource_pool.return_value = 0, "test"
        self.mock_resource_control.add_nodes_to_resource_pool.return_value = 0, "test"
        self.mock_provisioner.list.return_value = ['test1', 'test2', 'test3']
        self.mock_provisioner.list_images.return_value = ["Centos7.3", "Centos6", "Centos7.1"]
        self.mock_provisioner.add.return_value = 0
        self.mock_provisioner.set_image.return_value = 0
        self.mock_provisioner.set_kernel_args.return_value = 0
        self.mock_power_control.set_device_power_state.return_value = {'test1': True}

    def setup_mock_config(self):
        """mock configuration"""
        self.configuration_manager = MagicMock()

        self.bmc = {
            "ip_address": "localhost",
            "rest_server_port": "5000",
            "user": "root",
            "bios_images": "/tmp/images"
        }
        self.device1 = {
            "hostname": "test1",
            "ip_address": "192.168.1.1",
            "image": "old_img.bin",
            "provisioner_kernel_args": "old_diag",
            "console_port": "1000",
            "node_power": "mock",
            "device_type": "node",
            "pdu_list": "switch1",
            "bmc": self.bmc
        }

        self.device = {
            "hostname": "test1",
            "ip_address": "192.168.1.1",
            "image": "old_img.bin",
            "provisioner_kernel_args": "old_diag",
            "console_port": "1000",
            "resource_controller": "mock",
            "device_power_control": "mock",
            "provisioner": "mock",
            "node_power": "mock",
            "device_type": "node",
            "pdu_list": "switch1",
            "bmc": self.bmc
        }
        self.image_name = "Centos7.1"
        self.test_name = None
        self.image_name1 = "test2.bin"
        self.test_name1 = "test_diag.bin"

    @patch.object(MockConsoleLog, 'start_log_capture')
    def test_launch_diags_positive(self, console_mock):
        """Positive tests"""
        console_mock.start_log_capture = MagicMock()
        self.reset_for_test()
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        result = diags_mock_plugin.launch_diags(self.device, self.bmc)
        self.assertEqual('Diagnostics completed on node test1', result)

    def test_no_device(self):
        """tests exceptions"""
        self.reset_for_test()
        self.mock_provisioner.list.return_value = ['Node1', 'Node2']
        self.mock_provisioner.list_images.return_value = ["Centos7.3", "Centos6", "Centos7.1"]
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                Mock(), Mock(), self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name1, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

    def test_no_required_keys_exception(self):
        """tests exceptions"""
        self.reset_for_test()
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name1, test_name=self.test_name,
                                              plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device1, self.bmc)


    @patch.object(MockConsoleLog, 'start_log_capture')
    def test_provisioner_failures(self, console_mock):
        """tests exceptions"""
        console_mock.start_log_capture = MagicMock()
        self.reset_for_test()
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                Mock(), Mock(), self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name1, test_name=self.test_name1,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

        self.reset_for_test()
        self.mock_provisioner.set_kernel_args.side_effect = Exception
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                Mock(), Mock(), self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

        self.reset_for_test()
        self.mock_provisioner.list.side_effect = Exception
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                Mock(), Mock(), self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

    @patch.object(MockConsoleLog, 'start_log_capture')
    def test_power_control_failure(self, console_mock):
        """tests exceptions"""
        console_mock.start_log_capture = MagicMock()
        self.reset_for_test()
        self.mock_power_control.set_device_power_state.return_value = False
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

    @patch.object(MockConsoleLog, 'start_log_capture')
    def test_resource_failures(self, console_mock):
        """tests exceptions"""
        self.reset_for_test()
        console_mock.start_log_capture = MagicMock()
        self.mock_resource_control.add_nodes_to_resource_pool.return_value = 1, "test"
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

        self.reset_for_test()
        self.mock_resource_control.check_nodes_state.return_value = 1, "drain"
        self.mock_resource_control.remove_nodes_from_resource_pool.return_value = 1, 'test1'
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

        self.reset_for_test()
        self.mock_resource_control.check_nodes_state.return_value = 1, "idle"
        self.mock_resource_control.remove_nodes_from_resource_pool.return_value = 1, 'test1'
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)

    def test_parse_log(self):
        """tests exceptions"""
        self.reset_for_test()
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        diags_mock_plugin.device_name = 'test1'
        MockDiagnostics.Test_Status['test1'] = 'Done'

    def test_console_log_exception(self):
        """tests exceptions"""
        self.reset_for_test()
        self.mock_power_control.set_device_power_state.return_value = {'test1': False}
        self.mock_plugin_manager.create_instance.side_effect = [self.mock_provisioner, self.mock_resource_control,
                                                                self.mock_power_control]
        diags_mock_plugin = MockDiagnostics(diag_image=self.image_name, test_name=self.test_name,
                                            plugin_manager=self.mock_plugin_manager)
        with self.assertRaises(Exception):
            diags_mock_plugin.launch_diags(self.device, self.bmc)
