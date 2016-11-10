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
from ctrl.plugin.manager import PluginManager
from ctrl.commands.power_on.power_on import PluginMetadata as POn
from ctrl.commands.power_off.power_off import PluginMetadata as POff
from ctrl.commands.power_cycle.power_cycle import PluginMetadata as PCycle
from ctrl.commands.resource_pool_add.resource_pool_add import PluginMetadata as PRAdd
from ctrl.commands.resource_pool_remove.resource_pool_remove import \
    PluginMetadata as PRRemove
from ctrl.power_control.nodes.node_power import PluginMetadata as PNPower
from ctrl.bmc.ipmi_util.ipmi_util import PluginMetadata as PBmc
from ctrl.os_remote_access.ssh.ssh import PluginMetadata as PSsh


class CommandExeFactory(object):
    """This class contains all the functions exposed to cli code"""

    def __init__(self):
        self.invoker_ret_val = 0
        self.failed_device_name = list()
        self.manager = PluginManager()
        self.manager.add_provider(POn())
        self.manager.add_provider(POff())
        self.manager.add_provider(PCycle())
        self.manager.add_provider(PRAdd())
        self.manager.add_provider(PRRemove())
        self.manager.add_provider(PNPower())
        self.manager.add_provider(PBmc())
        self.manager.add_provider(PSsh())

    def device_name_check(self, device_name):
        """Check the device name & create a list"""
        if re.match("^[A-Za-z0-9,]+$", device_name):
            dev_list = device_name.split(",")
            return dev_list
        else:
            device_err_msg = "ERROR: Wrong Device Name/List. " \
                             "CtrlCli supports only comma separated list" \
                             "if device(s)"
            print(device_err_msg.format(device_err_msg))
            sys.exit(1)

    def create_dictionary(self, device_name, args):
        """Function to create dictionary for interface"""
        cmd_dictionary = {
            'device_name': device_name,
            'configuration': object(),
            'plugin_manager': self.manager,
            'logger': object(),
            'arguments': args
        }
        return cmd_dictionary

    def power_on_invoker(self, device_name, sub_command):
        """Execute Power On Command"""
        device_list = self.device_name_check(device_name)
        for device in device_list:
            cmd_dictionary = self.create_dictionary(device, sub_command)
            p_on_obj = self.manager.factory_create_instance('command',
                                                            'power_on',
                                                            cmd_dictionary)
            return_msg = p_on_obj.execute()
            print('{} - RETURN CODE: {}'.format(return_msg.message,
                                                return_msg.return_code))
            if return_msg.return_code != 0:
                self.invoker_ret_val = return_msg.return_code
                self.failed_device_name.append(device)
        return self.invoker_ret_val

    def power_off_invoker(self, device_name, sub_command):
        """Execute Power Off Command"""
        device_list = self.device_name_check(device_name)
        for device in device_list:
            cmd_dictionary = self.create_dictionary(device, sub_command)
            p_off_obj = self.manager.factory_create_instance('command',
                                                             'power_off',
                                                             cmd_dictionary)
            return_msg = p_off_obj.execute()
            print('{} - RETURN CODE: {}'.format(return_msg.message,
                                                return_msg.return_code))
            if return_msg.return_code != 0:
                self.invoker_ret_val = return_msg.return_code
                self.failed_device_name.append(device)
        return self.invoker_ret_val

    def power_cycle_invoker(self, device_name, sub_command):
        """Execute Power Reboot Command"""
        device_list = self.device_name_check(device_name)
        for device in device_list:
            cmd_dictionary = self.create_dictionary(device, sub_command)
            p_cycle_obj = self.manager.factory_create_instance('command',
                                                               'power_cycle',
                                                               cmd_dictionary)
            return_msg = p_cycle_obj.execute()
            print('{} - RETURN CODE: {}'.format(return_msg.message,
                                                return_msg.return_code))
            if return_msg.return_code != 0:
                self.invoker_ret_val = return_msg.return_code
                self.failed_device_name.append(device)
        return self.invoker_ret_val

    def resource_add_invoker(self, device_name, sub_command):
        """Execute Resource Add Command"""
        device_list = self.device_name_check(device_name)
        for device in device_list:
            cmd_dictionary = self.create_dictionary(device, sub_command)
            r_add_obj = self.manager.factory_create_instance('command',
                                                             'resource_pool_add',
                                                             cmd_dictionary)
            return_msg = r_add_obj.execute()
            print('{} - RETURN CODE: {}'.format(return_msg.message,
                                                return_msg.return_code))
            if return_msg.return_code != 0:
                self.invoker_ret_val = return_msg.return_code
                self.failed_device_name.append(device)
        return self.invoker_ret_val

    def resource_remove_invoker(self, device_name, sub_command):
        """Execute Resource Add Command"""
        device_list = self.device_name_check(device_name)
        for device in device_list:
            cmd_dictionary = self.create_dictionary(device, sub_command)
            r_remove_obj = self.manager.factory_create_instance('command',
                                                                'resource_pool_remove',
                                                                cmd_dictionary)
            return_msg = r_remove_obj.execute()
            print('{} - RETURN CODE: {}'.format(return_msg.message,
                                                return_msg.return_code))
            if return_msg.return_code != 0:
                self.invoker_ret_val = return_msg.return_code
                self.failed_device_name.append(device)
        return self.invoker_ret_val
