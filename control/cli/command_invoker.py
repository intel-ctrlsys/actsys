# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This module is called "Command Invoker" which uses APIs from "commands" folder
to perform user requested operations.
"""
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
from ..pdu.RaritanPX35180CR.RaritanPX35180CR import PluginMetadata as RaritanPluginMetadata
from ..pdu.IPS400.IPS400 import PluginMetadata as IPSPluginMetadata
from ..pdu.mock.mock import PluginMetadata as MockPduPluginMetadata
from ..resource.mock.mock_resource_control import PluginMetadata as MockPluginMetadata
from ..commands import CommandResult


class CommandInvoker(object):
    """This class contains all the functions exposed to cli code"""

    BASE_CLUSTER_CONFIG_NAME = "ctrl-config.json"

    def __init__(self):
        self.invoker_ret_val = 0
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
        home = os.path.join(os.getenv('HOME'), self.BASE_CLUSTER_CONFIG_NAME)
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
        self.manager.add_provider(RaritanPluginMetadata())
        self.manager.add_provider(IPSPluginMetadata())
        self.manager.add_provider(MockPduPluginMetadata())
        self.manager.add_provider(MockPluginMetadata())

    def common_cmd_invoker(self, device_name, sub_command, cmd_args=None):
        """Common Function to execute the user requested command"""
        if self.manager is None:
            self.init_manager()

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
        device_list = CommandInvoker._device_name_check(device_name)
        if not isinstance(device_list, list):
            result = CommandResult(1, "Failed to parse a valid device name(s) in {}".format(device_name))
            self.logger.warning(result.message)
            return result
        results = list()
        for device in device_list:
            if not self.device_exists_in_config(device):
                msg = "Device {} skipped, because it is not found in the config file.".format(device)
                self.logger.warning(msg)
                results.append(CommandResult(1, msg, device))
                continue

            cmd_dictionary = self.create_dictionary(device, cmd_args)
            cmd_obj = self.manager.factory_create_instance('command', command_map[sub_command], cmd_dictionary)
            self.logger.journal(cmd_obj)
            command_result = cmd_obj.execute()

            command_result.device_name = device
            self.logger.journal(cmd_obj, command_result)

            results.append(command_result)

        if len(results) == 1:
            return results[0]

        return results

    def device_exists_in_config(self, device_name):
        """Check if the device exists in the configuration file or not"""
        return self.extractor.get_device(device_name) is not None

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
