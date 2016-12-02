# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This module is called "Command Invoker" which uses APIs from "commands" folder
to perform user requested operations.
"""
from __future__ import print_function

import logging
import os
import re

from control.commands.resource_pool.resource_pool_add import \
    PluginMetadata as PRAdd
from control.commands.resource_pool.resource_pool_check import PluginMetadata as RCpluginMeta
from control.commands.resource_pool.resource_pool_remove import \
    PluginMetadata as PRRemove
from ..bmc.ipmi_util.ipmi_util import PluginMetadata as PBmc
from ..bmc.mock.bmc import PluginMetadata as PMockBmc
from ..commands.power.power_cycle.power_cycle import PluginMetadata as PCycle
from ..commands.power.power_off.power_off import PluginMetadata as POff
from ..commands.power.power_on.power_on import PluginMetadata as POn
from ..commands.services import ServicesStartPluginMetadata
from ..commands.services import ServicesStatusPluginMetadata
from ..commands.services import ServicesStopPluginMetadata
from ..configuration_manager.configuration_manager import ConfigurationManager
from ..ctrl_logger.ctrl_logger import get_ctrl_logger
from ..os_remote_access.mock.os_remote_access \
    import PluginMetadata as PMockSsh
from ..os_remote_access.ssh.ssh import PluginMetadata as PSsh
from ..plugin.manager import PluginManager
from ..power_control.mock.power_control_mock \
    import PluginMetadata as PMockNPower
from ..power_control.nodes.node_power import PluginMetadata as PNPower
from ..resource.slurm.slurm_resource_control import PluginMetadata as SlurmPluginMetadata


class CommandExeFactory(object):
    """This class contains all the functions exposed to cli code"""

    BASE_CLUSTER_CONFIG_NAME = "ctrl-config.json"

    def __init__(self):
        self.invoker_ret_val = 0
        self.sub_command_list = list()
        self.failed_device_name = list()
        self.logger = get_ctrl_logger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers[0].setLevel(logging.DEBUG)
        self.configuration = ConfigurationManager(file_path=self._get_correct_configuration_file())
        self.extractor = self.configuration.get_extractor()
        self.manager = None

    def _get_correct_configuration_file(self):
        """Resolve the configuration file if possible."""

        # Check for the file in the current working directory
        if os.path.isfile(self.BASE_CLUSTER_CONFIG_NAME):
            return os.path.join(os.path.curdir, self.BASE_CLUSTER_CONFIG_NAME)

        # check for file in ~/
        home = os.path.join(os.getenv('HOME'), '.' + self.BASE_CLUSTER_CONFIG_NAME)
        if os.path.isfile(home):
            return home

        # Check for the file in /etc/
        etc = '/etc/' + self.BASE_CLUSTER_CONFIG_NAME
        if os.path.isfile(etc):
            return etc

        # Failed to resolve, so return the base name... hopefully someone else can resolve it.
        self.logger.warning("The config file was not found in the current working directory, ~/ or /etc/.")
        return self.BASE_CLUSTER_CONFIG_NAME

    @classmethod
    def _device_name_check(cls, device_name):
        """Check the device name & create a list"""
        if re.match("^[A-Za-z0-9,\-]+$", device_name):
            dev_list = device_name.split(",")
            return dev_list
        else:
            device_err_msg = "ERROR: Wrong Device Name/List. " \
                             "ctrl supports only comma separated list" \
                             "if device(s)"
            print(device_err_msg.format(device_err_msg))
            return 1

    def create_dictionary(self, device_name, args):
        """Function to create dictionary for interface"""
        cmd_dictionary = {
            'device_name': device_name,
            'configuration': self.extractor,
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
        self.manager.add_provider(ServicesStatusPluginMetadata())
        self.manager.add_provider(ServicesStartPluginMetadata())
        self.manager.add_provider(ServicesStopPluginMetadata())
        self.manager.add_provider(RCpluginMeta())
        self.manager.add_provider(SlurmPluginMetadata())

    def common_cmd_invoker(self, device_name, sub_command, cmd_args=None):
        """Common Function to execute the user requested command"""
        # TODO: Move print statements out of this function, and into the CLI! (Nothing should ever
        #   print, it should only use the logger, or return its messages)
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
                       'resource_add': 'resource_pool_add',
                       'resource_remove': 'resource_pool_remove',
                       'resource_check': 'resource_pool_check',
                       'service_status': 'service_status',
                       'service_start': 'service_start',
                       'service_stop': 'service_stop'
                       }

        if cmd_args is not None:
            if cmd_args:
                self.sub_command_list.append('force')
        device_list = CommandExeFactory._device_name_check(device_name)
        if device_list == 1:
            self.logger.warning("Failed to parse a valid device name for {}".format(device_name))
            return 1
        for device in device_list:
            cmd_dictionary = self.create_dictionary(device,
                                                    self.sub_command_list)
            cmd_obj = self.manager.factory_create_instance('command',
                                                            command_map[
                                                                sub_command],
                                                            cmd_dictionary)
            self.logger.journal(cmd_obj)
            return_msg = cmd_obj.execute()
            self.logger.journal(cmd_obj, return_msg)

            print('{} - RETURN CODE: {}'.format(return_msg.message,
                                                return_msg.return_code))
            if return_msg.return_code != 0:
                self.invoker_ret_val = return_msg.return_code
                self.failed_device_name.append(device)

        if self.invoker_ret_val != 0:
            self.print_summary(self.failed_device_name)
        return self.invoker_ret_val

    def print_summary(self, failed_device_name):
        for failed_device in failed_device_name:
            print("\t*****************************")
            print("\t* COMMAND EXECUTION SUMMARY *")
            print("\t*****************************")
            print("\tFailed Device: {}".format(failed_device))

    def power_on_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Power On Command"""
        return self.common_cmd_invoker(device_name, sub_command, cmd_args)

    def power_off_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Power Off Command"""
        return self.common_cmd_invoker(device_name, sub_command, cmd_args)

    def power_cycle_invoker(self, device_name, sub_command, cmd_args=None):
        """Execute Power Reboot Command"""
        return self.common_cmd_invoker(device_name, sub_command, cmd_args)

    def resource_add(self, device_name, cmd_args=None):
        """Execute Resource Add Command"""
        return self.common_cmd_invoker(device_name, "resource_add", cmd_args)

    def resource_remove(self, device_name, cmd_args=None):
        """Execute Resource Add Command"""
        return self.common_cmd_invoker(device_name, "resource_remove", cmd_args)

    def resource_check(self, device_name, cmd_args=None):
        """Execute Resource Add Command"""
        return self.common_cmd_invoker(device_name, "resource_check", cmd_args)

    def service_status(self, device_name, cmd_args=None):
        """Execute a service check command"""
        return self.common_cmd_invoker(device_name, "service_status", cmd_args)

    def service_on(self, device_name, cmd_args=None):
        """Execute a service check command"""
        return self.common_cmd_invoker(device_name, "service_start", cmd_args)

    def service_off(self, device_name, cmd_args=None):
        """Execute a service check command"""
        return self.common_cmd_invoker(device_name, "service_stop", cmd_args)
