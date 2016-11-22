# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This module is called "Command Invoker" which uses APIs from "commands" folder
to perform user requested operations.
"""
from __future__ import print_function
import re
import sys
from ..plugin.manager import PluginManager
from ..commands.power.power_on.power_on import PluginMetadata as POn
from ..commands.power.power_off.power_off import PluginMetadata as POff
from ..commands.power.power_cycle.power_cycle import PluginMetadata as PCycle
from ..commands.resource_pool_add.resource_pool_add import \
    PluginMetadata as PRAdd
from ..commands.resource_pool_remove.resource_pool_remove import \
    PluginMetadata as PRRemove
from ..power_control.nodes.node_power import PluginMetadata as PNPower
from ..bmc.ipmi_util.ipmi_util import PluginMetadata as PBmc
from ..os_remote_access.ssh.ssh import PluginMetadata as PSsh
from ..os_remote_access.mock.os_remote_access \
    import PluginMetadata as PMockSsh
from ..power_control.mock.power_control_mock \
    import PluginMetadata as PMockNPower
from ..bmc.mock.bmc import PluginMetadata as PMockBmc
from ..ctrl_logger.ctrl_logger import CtrlLogger
from ..configuration_manager.configuration_manager import ConfigurationManager


class CommandExeFactory(object):
    """This class contains all the functions exposed to cli code"""

    def __init__(self):
        self.invoker_ret_val = 0
        self.sub_command_list = list()
        self.failed_device_name = list()
        self.logger = CtrlLogger()
        self.configuration = ConfigurationManager(file_path='/configuration_manager'
                                                            '/json_parser/tests/'
                                                            'file.json')
        self.manager = None

    @classmethod
    def _device_name_check(cls, device_name):
        """Check the device name & create a list"""
        if re.match("^[A-Za-z0-9,]+$", device_name):
            dev_list = device_name.split(",")
            return dev_list
        else:
            device_err_msg = "ERROR: Wrong Device Name/List. " \
                             "CtrlCli supports only comma separated list" \
                             "if device(s)"
            print(device_err_msg.format(device_err_msg))
            return 1

    def create_dictionary(self, device_name, args):
        """Function to create dictionary for interface"""
        cmd_dictionary = {
            'device_name': device_name,
            'configuration': self.configuration,
            'plugin_manager': self.manager,
            'logger': self.logger,
            'arguments': args
        }
        return cmd_dictionary

    def init_manager(self):
        self.manager = PluginManager()
        self.manager.add_provider(POn())
        self.manager.add_provider(POff())
        self.manager.add_provider(PCycle())
        self.manager.add_provider(PRAdd())
        self.manager.add_provider(PRRemove())
        self.manager.add_provider(PNPower())
        self.manager.add_provider(PBmc())
        self.manager.add_provider(PSsh())
        self.manager.add_provider(PMockSsh())
        self.manager.add_provider(PMockNPower())
        self.manager.add_provider(PMockBmc())

    def common_cmd_invoker(self, device_name, sub_command, cmd_args=None):
        """Common Function to execute the user requested command"""

        if self.manager is None:
            self.init_manager()

        self.sub_command_list.append(sub_command)

        command_map = {'on': 'power_on',
                       'off': 'power_off',
                       'cycle': 'power_cycle',
                       'bios': 'power_cycle',
                       'efi': 'power_cycle',
                       'hdd': 'power_cycle',
                       'pxe': 'power_cycle',
                       'cdrom': 'power_cycle',
                       'removable': 'power_cycle',
                       'add': 'resource_pool_add',
                       'remove': 'resource_pool_remove'
                       }

        if cmd_args is not None:
            if cmd_args:
                self.sub_command_list.append('force')
        device_list = CommandExeFactory._device_name_check(device_name)
        for device in device_list:
            cmd_dictionary = self.create_dictionary(device,
                                                    self.sub_command_list)
            p_on_obj = self.manager.factory_create_instance('command',
                                                            command_map[
                                                                sub_command],
                                                            cmd_dictionary)
            return_msg = p_on_obj.execute()
            print('{} - RETURN CODE: {}'.format(return_msg.message,
                                                return_msg.return_code))
            if return_msg.return_code != 0:
                self.invoker_ret_val = return_msg.return_code
                self.failed_device_name.append(device)
        return self.invoker_ret_val

    def print_summary(self, failed_device_name):
        for failed_device in failed_device_name:
            print("\t*****************************")
            print("\t* COMMAND EXECUTION SUMMARY *")
            print("\t*****************************")
            print("\tFailed Device: {}".format(failed_device))

    def power_on_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Power On Command"""
        retval = self.common_cmd_invoker(device_name, sub_command, cmd_args)
        if retval != 0:
            self.print_summary(self.failed_device_name)
        return retval

    def power_off_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Power Off Command"""
        retval = self.common_cmd_invoker(device_name, sub_command, cmd_args)
        if retval != 0:
            self.print_summary(self.failed_device_name)
        return retval

    def power_cycle_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Power Reboot Command"""
        retval = self.common_cmd_invoker(device_name, sub_command, cmd_args)
        if retval != 0:
            self.print_summary(self.failed_device_name)
        return retval

    def resource_add_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Resource Add Command"""
        retval = self.common_cmd_invoker(device_name, sub_command, cmd_args)
        if retval != 0:
            self.print_summary(self.failed_device_name)
        return retval

    def resource_remove_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Resource Add Command"""
        retval = self.common_cmd_invoker(device_name, sub_command, cmd_args)
        if retval != 0:
            self.print_summary(self.failed_device_name)
        return retval
