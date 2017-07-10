# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
from __future__ import print_function
import sys
from unittest import TestCase

from mock import patch, MagicMock

from ..command_invoker import CommandInvoker
from ..control_cli import ControlArgParser, ControlCommandLineInterface
from ...commands import CommandResult
from datastore.utilities import FileNotFound, DeviceUtilities


class CommandInvokerTest(TestCase):
    @patch("control.cli.CommandInvoker")
    def setUp(self, mock_command_invoker):
        self.original_cluster_config_name = CommandInvoker.CTRL_CONFIG_LOCATION
        CommandInvoker.CTRL_CONFIG_LOCATION = "ctrl-config-example.json"
        self.TestParser = ControlArgParser()
        self.control_cli_executor = ControlCommandLineInterface()

        mock_command_invoker.resource_check.return_value = CommandResult(0)
        mock_command_invoker.resource_remove.return_value = CommandResult(0)
        mock_command_invoker.resource_add.return_value = CommandResult(0)
        mock_command_invoker.service_status.return_value = CommandResult(0)
        mock_command_invoker.service_off.return_value = CommandResult(0)
        mock_command_invoker.service_on.return_value = CommandResult(0)
        mock_command_invoker.power_on_invoker.return_value = CommandResult(0)
        mock_command_invoker.power_off_invoker.return_value = CommandResult(0)
        mock_command_invoker.power_cycle_invoker.return_value = CommandResult(0)
        mock_command_invoker.bios_update.return_value = CommandResult(0)

        self.control_cli_executor.cmd_invoker = mock_command_invoker

    def tearDown(self):
        CommandInvoker.BASE_CLUSTER_CONFIG_NAME = self.original_cluster_config_name

    def test_resource_check_cmd_execute(self):
        sys.argv[1:] = ['resource', 'check', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.resource_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_resource_remove_cmd_execute(self):
        sys.argv[1:] = ['resource', 'remove', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.resource_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_resource_add_cmd_execute(self):
        sys.argv[1:] = ['resource', 'add', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.resource_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_service_start_cmd_execute(self):
        sys.argv[1:] = ['service', 'start', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.service_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_service_check_cmd_execute(self):
        sys.argv[1:] = ['service', 'status', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.service_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_service_remove_cmd_execute(self):
        sys.argv[1:] = ['service', 'stop', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.service_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_power_off_cmd_execute(self):
        sys.argv[1:] = ['power', 'off', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.power_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_power_cycle_cmd_execute(self):
        sys.argv[1:] = ['power', 'cycle', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.power_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_power_on_cmd_execute(self):
        sys.argv[1:] = ['power', 'on', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = self.control_cli_executor.power_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_process_list_cmd_execute(self):
        sys.argv[1:] = ['process', 'list', 'compute-29', '178']
        test_args = self.TestParser.get_all_args()
        ret = ControlCommandLineInterface().process_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_process_kill_cmd_execute(self):
        sys.argv[1:] = ['process', 'kill', 'compute-29', '178']
        test_args = self.TestParser.get_all_args()
        ret = ControlCommandLineInterface().process_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_get_freq_cmd_execute(self):
        sys.argv[1:] = ['get', 'freq', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = ControlCommandLineInterface().get_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_get_power_cmd_execute(self):
        sys.argv[1:] = ['get', 'powercap', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = ControlCommandLineInterface().get_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_set_freq_cmd_execute(self):
        sys.argv[1:] = ['set', 'freq', 'compute-29', '452']
        test_args = self.TestParser.get_all_args()
        ret = ControlCommandLineInterface().set_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_set_power_cmd_execute(self):
        sys.argv[1:] = ['set', 'powercap', 'compute-29', '452']
        test_args = self.TestParser.get_all_args()
        ret = ControlCommandLineInterface().set_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)

    def test_bios_update_cmd_execute(self):
        sys.argv[1:] = ['bios', 'update', 'compute-29']
        test_args = self.TestParser.get_all_args()
        ret = ControlCommandLineInterface().set_cmd_execute(test_args)
        self.assertEqual(ret.return_code, 0)


class CommandExeFactoryTest(TestCase):
    @patch("control.plugin.manager.PluginManager")
    def setUp(self, mock_plugin_manager):
        self.TestParser = ControlArgParser()
        self.original_cluster_config_name = CommandInvoker.CTRL_CONFIG_LOCATION
        CommandInvoker.CTRL_CONFIG_LOCATION = "ctrl-config-example.json"
        self.command_invoker = CommandInvoker()
        self.command_invoker.logger = MagicMock()
        self.mock_plugin_manager = mock_plugin_manager
        self.mock_plugin_manager.create_instance.return_value.execute. \
            return_value = CommandResult(0)
        self.command_invoker.manager = self.mock_plugin_manager

        self.get_device = self.command_invoker.datastore.get_device
        self.command_invoker.datastore.get_device = self.returns_true

    def tearDown(self):
        self.command_invoker.datastore.get_device = self.get_device
        CommandInvoker.CTRL_CONFIG_LOCATION = self.original_cluster_config_name

    def returns_true(self, device_name):
        return True

    def mock_init_manager(self):
        self.command_invoker.manager = self.mock_plugin_manager

    def test_manager_is_created(self):
        self.command_invoker.manager = None
        self.command_invoker.init_manager()

        self.assertIsNotNone(self.command_invoker.manager)

    def test_wrong_device_name(self):
        device_name = 'compute-29['
        with self.assertRaises(DeviceUtilities.DeviceListParseError):
            ret_val = CommandInvoker()._device_name_check(device_name)

    def test_wrong_device_name2(self):
        self.command_invoker.datastore.get_device = self.get_device
        retval = self.command_invoker.service_status("co!m@pute-29")
        self.assertEqual(retval.return_code, 1)

    def test_correct_device_name(self):
        device_name = "compute-29"
        dev_list = CommandInvoker()._device_name_check(device_name)
        self.assertEqual(device_name, dev_list[0])

    def test_poweron_invoker(self):
        device_name = "compute-29"
        sub_command = "on"

        retval = self.command_invoker.power_on_invoker(device_name, sub_command)
        print (retval)
        self.assertEqual(retval.return_code, 0)

    def test_poweron_force_invoker(self):
        device_name = "compute-29"
        sub_command = "on"
        sys.argv[1:] = ['power', 'on', '-f', 'compute-29']
        cmd_args = self.TestParser.get_all_args()
        retval = self.command_invoker.power_on_invoker(device_name, sub_command, cmd_args)
        self.assertEqual(retval.return_code, 0)

    def test_powercycle_invoker(self):
        device_name = "compute-31"
        sub_command = "cycle"
        retval = self.command_invoker.power_cycle_invoker(device_name, sub_command)
        self.assertEqual(retval.return_code, 0)

    def test_poweroff_invoker(self):
        device_name = "compute-29,compute-30"
        sub_command = "off"
        retval = self.command_invoker.power_off_invoker(device_name, sub_command)
        self.assertEqual(retval.return_code, 0)
        self.assertEqual(retval.return_code, 0)

    def test_resource_add_invoker(self):
        device_name = "compute-29,compute-30"
        sub_command = "add"
        retval = self.command_invoker.resource_add(device_name)
        self.assertEqual(retval.return_code, 0)

    def test_resource_remove_invoker(self):
        device_name = "compute-29,compute-30"
        retval = self.command_invoker.resource_remove(device_name)
        self.assertEqual(retval.return_code, 0)

    def test_resource_check_invoker(self):
        device_name = "compute-29,compute-30"
        retval = self.command_invoker.resource_check(device_name)
        self.assertEqual(retval.return_code, 0)

    def test_service_status(self):
        retval = self.command_invoker.service_status("compute-29")
        self.assertEqual(retval.return_code, 0)
        retval = self.command_invoker.service_status("compute-29,compute-30")
        self.assertEqual(retval.return_code, 0)
        self.assertEqual(retval.return_code, 0)

    def test_service_status2(self):
        self.command_invoker.manager = None
        old_func = self.command_invoker.init_manager
        self.command_invoker.init_manager = self.mock_init_manager
        # self.cmd_exe_factory_obj.extractor.get_device = self.get_device

        retval = self.command_invoker.service_status("compute-29")
        self.assertEqual(retval.return_code, 0)
        retval = self.command_invoker.service_status("compute-29,compute-30")
        self.assertEqual(retval.return_code, 0)
        self.assertEqual(retval.return_code, 0)
        self.command_invoker.init_manager = old_func

    def test_service_on(self):
        retval = self.command_invoker.service_on("compute-29")
        self.assertEqual(retval.return_code, 0)
        retval = self.command_invoker.service_on("compute-29,compute-30")
        self.assertEqual(retval.return_code, 0)
        self.assertEqual(retval.return_code, 0)

    def test_service_off(self):
        retval = self.command_invoker.service_off("compute-29")
        self.assertEqual(retval.return_code, 0)
        retval = self.command_invoker.service_off("compute-29,compute-30")
        self.assertEqual(retval.return_code, 0)
        self.assertEqual(retval.return_code, 0)


class ControlCliParserTest(TestCase):
    @patch("control.plugin.manager.PluginManager")
    def setUp(self, mock_plugin_manager):
        self.TestParser = ControlArgParser()
        self.original_cluster_config_name = CommandInvoker.BASE_CLUSTER_CONFIG_NAME
        CommandInvoker.BASE_CLUSTER_CONFIG_NAME = "ctrl-config-example.json"
        CommandInvoker.POSTGRES_ENV_VAR = "NOT_VALID"
        self.command_invoker = CommandInvoker()
        self.command_invoker.logger = MagicMock()
        mock_plugin_manager.create_instance.return_value.execute. \
            return_value = CommandResult(0)
        self.command_invoker.manager = mock_plugin_manager

    def tearDown(self):
        CommandInvoker.BASE_CLUSTER_CONFIG_NAME = self.original_cluster_config_name

    def test_version(self):
        sys.argv[1:] = ['--version']
        with self.assertRaises(SystemExit):
            self.TestParser.get_all_args()

    def test_power_on_only(self):
        sys.argv[1:] = ['power', 'on', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "on")

    def test_power_off_only(self):
        sys.argv[1:] = ['power', 'off', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "off")

    def test_power_cycle_only(self):
        sys.argv[1:] = ['power', 'cycle', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "cycle")

    def test_resource_add_only(self):
        sys.argv[1:] = ['resource', 'add', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "add")

    def test_resource_remove_only(self):
        sys.argv[1:] = ['resource', 'remove', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "remove")

    def test_resource_check_only(self):
        sys.argv[1:] = ['resource', 'check', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "check")

    def test_process_list_only(self):
        sys.argv[1:] = ['process', 'list', '387', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "list")

    def test_process_kill_only(self):
        sys.argv[1:] = ['process', 'kill', '387', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "kill")

    def test_get_freq_only(self):
        sys.argv[1:] = ['get', 'freq', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "freq")

    def test_get_powercap_only(self):
        sys.argv[1:] = ['get', 'powercap', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "powercap")

    def test_set_freq_only(self):
        sys.argv[1:] = ['set', 'freq', '127', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "freq")

    def test_set_powercap_only(self):
        sys.argv[1:] = ['set', 'powercap', '127', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "powercap")

    def test_bios_update_only(self):
        sys.argv[1:] = ['bios', 'update', '-i test.bin', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "update")

    def test_bios_version_only(self):
        sys.argv[1:] = ['bios', 'get-version', 'compute-29']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "get-version")

    @patch("control.cli.CommandInvoker.__init__", MagicMock(side_effect=RuntimeError("Error")))
    def test_init_exception(self):
        with self.assertRaises(SystemExit):
            ControlCommandLineInterface().execute_cli_cmd()

    @patch("control.cli.CommandInvoker.__init__",
           MagicMock(side_effect=FileNotFound("Error_file_path")))
    def test_init_exception2(self):
        with self.assertRaises(SystemExit):
            ControlCommandLineInterface().execute_cli_cmd()

    def test_resource_invalid_command(self):
        sys.argv[1:] = ['resource', 'foo', 'compute-29']
        with self.assertRaises(SystemExit):
            test_args = self.TestParser.get_all_args()
            ret = ControlCommandLineInterface().resource_cmd_execute(test_args)

    def test_service_invalid_command(self):
        sys.argv[1:] = ['service', 'foo', 'compute-29']
        with self.assertRaises(SystemExit):
            test_args = self.TestParser.get_all_args()
            ControlCommandLineInterface().resource_cmd_execute(test_args)

    @patch.object(ControlCommandLineInterface, "power_cmd_execute")
    def test_exe_cli_cmd_with_power(self, mock_pwr_cmd_exe):
        sys.argv[1:] = ['power', 'on', 'compute-29']
        mock_pwr_cmd_exe.return_value = CommandResult(0)
        retval = ControlCommandLineInterface().execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_exe_cli_cmd_with_process(self):
        sys.argv[1:] = ['process', 'list', 'compute-29', '178']
        retval = ControlCommandLineInterface().execute_cli_cmd()
        self.assertEqual(retval, 0)

    @patch.object(ControlCommandLineInterface, "resource_cmd_execute")
    def test_exe_cli_cmd_with_resource(self, mock_rce):
        sys.argv[1:] = ['resource', 'add', 'compute-29']
        mock_rce.return_value = CommandResult(0)
        self.assertEqual(ControlCommandLineInterface().execute_cli_cmd(), 0)

    @patch.object(ControlCommandLineInterface, "service_cmd_execute")
    def test_exe_cli_cmd_with_service(self, mock_sce):
        sys.argv[1:] = ['service', 'status', 'compute-29']
        mock_sce.return_value = CommandResult(0)
        self.assertEqual(ControlCommandLineInterface().execute_cli_cmd(), 0)

    @patch.object(ControlCommandLineInterface, "bios_cmd_execute")
    def test_exe_cli_with_bios(self, mock_bios):
        sys.argv[1:] = ['bios', 'update','-i /tmp/test.bin', 'compute-29']
        mock_bios.return_value = CommandResult(0)
        self.assertEqual(ControlCommandLineInterface().execute_cli_cmd(), 0)

    def test_exe_cli_cmd_with_get(self):
        sys.argv[1:] = ['get', 'freq', 'compute-29']
        retval = ControlCommandLineInterface().execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_exe_cli_cmd_with_set(self):
        sys.argv[1:] = ['set', 'freq', 'compute-29', '452']
        retval = ControlCommandLineInterface().execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_z_pon_neg(self):
        sys.argv[1:] = ['power', 'on', '-f', 'compute-29']
        test_args = self.TestParser.get_all_args()
        args = CommandResult(message='pass', return_code=1)
        device_name = "compute-29,compute-30"
        sub_command = "on"
        self.command_invoker.manager.create_instance.return_value.execute.return_value.return_code = 1
        retval = self.command_invoker.power_on_invoker(device_name, sub_command,
                                                       test_args)
        self.assertNotEqual(retval.return_code, 0)
        self.assertNotEqual(retval.return_code, 0)

    def test_z_poff_neg(self):
        args = CommandResult(message='pass', return_code=1)
        device_name = "compute-30,compute-29"
        sub_command = "off"
        self.command_invoker.manager.create_instance.return_value.execute.return_value.return_code = 1
        retval = self.command_invoker.power_off_invoker(device_name, sub_command)
        self.assertNotEqual(retval.return_code, 0)
        self.assertNotEqual(retval.return_code, 0)

    def test_z_pre_neg(self):
        args = CommandResult(message='pass', return_code=1)
        device_name = "compute-29,compute-30"
        sub_command = "cycle"
        self.command_invoker.manager.create_instance.return_value.execute.return_value.return_code = 1
        retval = self.command_invoker.power_cycle_invoker(device_name,
                                                          sub_command)
        print("RETURN: {}".format(retval))
        self.assertNotEqual(retval, 0)

    def test_z_readd_neg(self):
        args = CommandResult(message='pass', return_code=1)
        device_name = "compute-29,compute-30"
        sub_command = "add"
        self.command_invoker.manager.create_instance.return_value.execute.return_value.return_code = 1
        retval = self.command_invoker.resource_add(device_name)
        print("RETURN: {}".format(retval))
        self.assertNotEqual(retval, 0)

    def test_z_rerm_neg(self):
        args = CommandResult(message='pass', return_code=1)
        device_name = "compute-29,compute-30"
        sub_command = "remove"
        self.command_invoker.manager.create_instance.return_value.execute.return_value.return_code = 1
        retval = self.command_invoker.resource_remove(device_name)
        print("RETURN: {}".format(retval))
        self.assertNotEqual(retval, 0)

    def test_invalid_device_name(self):
        device_name = "non-existant-node-1"
        self.command_invoker.manager.create_instance.return_value.execute.return_value.return_code = 1
        retval = self.command_invoker.resource_remove(device_name)
        self.assertEqual(retval.return_code, 1)

    def test_invalid_device_name2(self):
        device_name = "non-existant-node-1,compute-30"
        self.command_invoker.manager.create_instance.return_value.execute.side_effect = [
            CommandResult(1), CommandResult(0)]
        retval = self.command_invoker.resource_remove(device_name)
        self.assertEqual(retval[0].return_code, 1)

    def test_handle_command_result(self):
        ctrl_cli_executor = ControlCommandLineInterface()
        return_code = ctrl_cli_executor.handle_command_result(CommandResult(0))
        self.assertEqual(return_code, 0)
        return_code = ctrl_cli_executor.handle_command_result(CommandResult(1))
        self.assertEqual(return_code, 1)
        return_code = ctrl_cli_executor.handle_command_result(CommandResult(2))
        self.assertEqual(return_code, 2)
        return_code = ctrl_cli_executor.handle_command_result(CommandResult(3))
        self.assertEqual(return_code, 3)

    def test_handle_command_result_multiple(self):
        ctrl_cli_executor = ControlCommandLineInterface()
        ctrl_cli_executor.cmd_invoker = self.command_invoker
        return_code = ctrl_cli_executor.handle_command_result([CommandResult(0), CommandResult(0)])
        self.assertEqual(return_code, 0)
        return_code = ctrl_cli_executor.handle_command_result([CommandResult(1), CommandResult(0)])
        self.assertEqual(return_code, 1)
        return_code = ctrl_cli_executor.handle_command_result([CommandResult(0), CommandResult(2)])
        self.assertEqual(return_code, 1)
        return_code = ctrl_cli_executor.handle_command_result([CommandResult(3), CommandResult(127)])
        self.assertEqual(return_code, 2)