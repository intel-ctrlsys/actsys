# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#

from unittest import TestCase
import sys
from ctrl.cli.control_cli import CtrlCliParser, CtrlCliExecutor
from ctrl.cli.cli_cmd_invoker import CommandExeFactory
from ctrl.commands.power_on import PowerOnCommand
from ctrl.commands.power_off import PowerOffCommand
from ctrl.commands.power_cycle import PowerCycleCommand
from ctrl.commands.resource_pool_add import ResourcePoolAddCommand
from ctrl.commands.resource_pool_remove import ResourcePoolRemoveCommand
from mock import patch
from ctrl.commands.command import CommandResult


class ControlCliParserTest(TestCase):

    @patch("plugin.manager.PluginManager")
    def setUp(self, mock_plugin_manager):
        self.TestParser = CtrlCliParser()
        self.cmd_exe_factory_obj = CommandExeFactory()
        mock_plugin_manager.factory_create_instance.return_value.execute.\
            return_value.return_code = 0
        self.cmd_exe_factory_obj.manager = mock_plugin_manager

    def test_version(self):
        sys.argv[1:] = ['--version']
        with self.assertRaises(SystemExit):
            self.TestParser.get_all_args()

    def test_power_on_only(self):
        sys.argv[1:] = ['power', 'on', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "on")

    def test_power_off_only(self):
        sys.argv[1:] = ['power', 'off', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "off")

    def test_power_cycle_only(self):
        sys.argv[1:] = ['power', 'cycle', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "cycle")

    def test_resource_add_only(self):
        sys.argv[1:] = ['resource', 'add', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "add")

    def test_resource_remove_only(self):
        sys.argv[1:] = ['resource', 'remove', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "remove")

    def test_process_list_only(self):
        sys.argv[1:] = ['process', 'list', '387', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "list")

    def test_process_kill_only(self):
        sys.argv[1:] = ['process', 'kill', '387', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "kill")

    def test_get_freq_only(self):
        sys.argv[1:] = ['get', 'freq', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "freq")

    def test_get_powercap_only(self):
        sys.argv[1:] = ['get', 'powercap', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "powercap")

    def test_set_freq_only(self):
        sys.argv[1:] = ['set', 'freq', '127', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "freq")

    def test_set_powercap_only(self):
        sys.argv[1:] = ['set', 'powercap', '127', 'n01']
        test_args = self.TestParser.get_all_args()
        self.assertEqual(test_args.subcommand, "powercap")

    @patch("cli.cli_cmd_invoker.CommandExeFactory")
    def test_power_on_cmd_execute(self, mock_cmd_exe_factory):
        sys.argv[1:] = ['power', 'on', 'n01']
        test_args = self.TestParser.get_all_args()
        ctrl_cli_exe_obj = CtrlCliExecutor()
        mock_cmd_exe_factory.power_on_invoker.return_value = 0
        ctrl_cli_exe_obj.cmd_exe_factory_obj = mock_cmd_exe_factory
        ret = ctrl_cli_exe_obj.power_cmd_execute(test_args)
        print"RETURN: {}" .format(ret)
        self.assertEqual(ret, 0)

    @patch("cli.cli_cmd_invoker.CommandExeFactory")
    def test_power_off_cmd_execute(self, mock_cmd_exe_factory):
        sys.argv[1:] = ['power', 'off', 'n01']
        test_args = self.TestParser.get_all_args()
        ctrl_cli_exe_object = CtrlCliExecutor()
        mock_cmd_exe_factory.power_off_invoker.return_value = 0
        ctrl_cli_exe_object.cmd_exe_factory_obj = mock_cmd_exe_factory
        ret = ctrl_cli_exe_object.power_cmd_execute(test_args)
        print"RETURN: {}" .format(ret)
        self.assertEqual(ret, 0)

    @patch("cli.cli_cmd_invoker.CommandExeFactory")
    def test_power_cycle_cmd_execute(self, mock_cmd_exe_factory):
        sys.argv[1:] = ['power', 'cycle', 'n01']
        test_args = self.TestParser.get_all_args()
        ctrl_cli_exe_obj = CtrlCliExecutor()
        mock_cmd_exe_factory.power_cycle_invoker.return_value = 0
        ctrl_cli_exe_obj.cmd_exe_factory_obj = mock_cmd_exe_factory
        ret = ctrl_cli_exe_obj.power_cmd_execute(test_args)
        print"RETURN: {}" .format(ret)
        self.assertEqual(ret, 0)

    def test_resource_add_cmd_execute(self):
        sys.argv[1:] = ['resource', 'add', 'n01']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().resource_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_resource_remove_cmd_execute(self):
        sys.argv[1:] = ['resource', 'remove', 'n01']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().resource_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_process_list_cmd_execute(self):
        sys.argv[1:] = ['process', 'list', 'n01', '178']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().process_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_process_kill_cmd_execute(self):
        sys.argv[1:] = ['process', 'kill', 'n01', '178']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().process_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_get_freq_cmd_execute(self):
        sys.argv[1:] = ['get', 'freq', 'n01']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().get_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_get_power_cmd_execute(self):
        sys.argv[1:] = ['get', 'powercap', 'n01']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().get_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_set_freq_cmd_execute(self):
        sys.argv[1:] = ['set', 'freq', 'n01', '452']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().set_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_set_power_cmd_execute(self):
        sys.argv[1:] = ['set', 'powercap', 'n01', '452']
        test_args = self.TestParser.get_all_args()
        ret = CtrlCliExecutor().set_cmd_execute(test_args)
        self.assertEqual(ret, 0)

    def test_wrong_device_name(self):
        device_name = 'n01#'
        ret_val = CommandExeFactory()._device_name_check(device_name)
        self.assertEqual(ret_val, 1)

    def test_correct_device_name(self):
        device_name = "n01"
        dev_list = CommandExeFactory()._device_name_check(device_name)
        self.assertEqual(device_name, dev_list[0])

    @patch.object(CtrlCliExecutor, "power_cmd_execute")
    def test_exe_cli_cmd_with_power(self, mock_pwr_cmd_exe):
        sys.argv[1:] = ['power', 'on', 'n01']
        ctrl_cli_exe_obj = CtrlCliExecutor()
        mock_pwr_cmd_exe.return_value = 0
        retval = ctrl_cli_exe_obj.execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_exe_cli_cmd_with_process(self):
        sys.argv[1:] = ['process', 'list', 'n01', '178']
        retval = CtrlCliExecutor().execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_exe_cli_cmd_with_resource(self):
        sys.argv[1:] = ['resource', 'add', 'n01']
        retval = CtrlCliExecutor().execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_exe_cli_cmd_with_get(self):
        sys.argv[1:] = ['get', 'freq', 'n01']
        retval = CtrlCliExecutor().execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_exe_cli_cmd_with_set(self):
        sys.argv[1:] = ['set', 'freq', 'n01', '452']
        retval = CtrlCliExecutor().execute_cli_cmd()
        self.assertEqual(retval, 0)

    def test_poweron_invoker(self):
        device_name = "n01"
        sub_command = "on"
        retval = self.cmd_exe_factory_obj.power_on_invoker(device_name, sub_command)
        self.assertEqual(retval, 0)

    def test_poweron_force_invoker(self):
        device_name = "n01"
        sub_command = "on"
        sys.argv[1:] = ['power', 'on', '-f', 'n01']
        cmd_args = self.TestParser.get_all_args()
        retval = self.cmd_exe_factory_obj.power_on_invoker(device_name, sub_command, cmd_args)
        self.assertEqual(retval, 0)

    def test_powercycle_invoker(self):
        device_name = "n03"
        sub_command = "cycle"
        retval = self.cmd_exe_factory_obj.power_cycle_invoker(device_name, sub_command)
        self.assertEqual(retval, 0)

    def test_poweroff_invoker(self):
        device_name = "n01,n02"
        sub_command = "off"
        retval = self.cmd_exe_factory_obj.power_off_invoker(device_name, sub_command)
        print"RETURN: {}" .format(retval)
        self.assertEqual(retval, 0)

    @patch.object(ResourcePoolAddCommand, 'execute')
    def test_resourceadd_invoker(self, MockResourcePoolAddCommand_execute):
        args = CommandResult(message='pass', return_code=0)
        device_name = "n01,n02"
        sub_command = "add"
        MockResourcePoolAddCommand_execute.return_value = args
        retval = CommandExeFactory().resource_add_invoker(device_name,
                                                          sub_command)
        print"RETURN: {}" .format(retval)
        self.assertEqual(retval, 0)

    @patch.object(ResourcePoolRemoveCommand, 'execute')
    def test_resourceremove_invoker(self, MockResourcePoolRemoveCommand_execute):
        args = CommandResult(message='pass', return_code=0)
        device_name = "n01,n02"
        sub_command = "remove"
        MockResourcePoolRemoveCommand_execute.return_value = args
        retval = CommandExeFactory().resource_remove_invoker(device_name,
                                                             sub_command)
        print "RETURN: {}" .format(retval)
        self.assertEqual(retval, 0)

    @patch('ctrl.commands.power_on.power_on.PowerOnCommand')
    def test_z_pon_neg(self, MockPowerOnCommand):
        sys.argv[1:] = ['power', 'on', '-f', 'n01']
        test_args = self.TestParser.get_all_args()
        args = CommandResult(message='pass', return_code=1)
        device_name = "n01,n02"
        sub_command = "on"
        MockPowerOnCommand.execute.return_value = args
        retval = CommandExeFactory().power_on_invoker(device_name, sub_command,
                                                      test_args)
        print"RETURN: {}" .format(retval)
        self.assertNotEqual(retval, 0)

    @patch('ctrl.commands.power_off.power_off.PowerOffCommand')
    def test_z_poff_neg(self, MockPowerOffCommand):
        args = CommandResult(message='pass', return_code=1)
        device_name = "n01,n02"
        sub_command = "off"
        MockPowerOffCommand.execute.return_value = 1
        retval = CommandExeFactory().power_off_invoker(device_name, sub_command)
        print"RETURN: {}" .format(retval)
        self.assertNotEqual(retval, 0)

    @patch('ctrl.commands.power_cycle.power_cycle.PowerCycleCommand')
    def test_z_pre_neg(self, MockPowerCycleCommand):
        args = CommandResult(message='pass', return_code=1)
        device_name = "n01,n02"
        sub_command = "cycle"
        MockPowerCycleCommand.execute.return_value = 1
        retval = CommandExeFactory().power_cycle_invoker(device_name,
                                                         sub_command)
        print"RETURN: {}" .format(retval)
        self.assertNotEqual(retval, 0)

    @patch('ctrl.commands.resource_pool_add.resource_pool_add.'
           'ResourcePoolAddCommand')
    def test_z_readd_neg(self, MockResourcePoolAddCommand):
        args = CommandResult(message='pass', return_code=1)
        device_name = "n01,n02"
        sub_command = "add"
        MockResourcePoolAddCommand.execute.return_value = 1
        retval = CommandExeFactory().resource_add_invoker(device_name,
                                                          sub_command)
        print"RETURN: {}" .format(retval)
        self.assertNotEqual(retval, 0)

    @patch('ctrl.commands.resource_pool_remove.resource_pool_remove.'
           'ResourcePoolRemoveCommand')
    def test_z_rerm_neg(self, MockResourcePoolRemoveCommand):
        args = CommandResult(message='pass', return_code=1)
        device_name = "n01,n02"
        sub_command = "remove"
        MockResourcePoolRemoveCommand.execute.return_value = 1
        retval = CommandExeFactory().resource_remove_invoker(device_name,
                                                             sub_command)
        print"RETURN: {}" .format(retval)
        self.assertNotEqual(retval, 0)
