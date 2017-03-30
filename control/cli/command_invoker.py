# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
This module is called "Command Invoker" which uses APIs from "commands" folder
to perform user requested operations.
"""
from __future__ import print_function
import os
import re
import logging
from ..plugin.manager import PluginManager
from ..commands import CommandResult
from datastore import DataStoreBuilder


class CommandInvoker(object):
    """This class contains all the functions exposed to cli code"""

    BASE_CLUSTER_CONFIG_NAME = "ctrl-config.json"
    POSTGRES_ENV_VAR = "CTRL_POSTGRES_CONNECTION_STRING"
    FILE_LOCATION_ENV_VAR = "CTRL_CONFIG_FILE"
    POSTGRES_CONNECTION_STRING = None

    def __init__(self):
        self.invoker_ret_val = 0
        self.failed_device_name = list()

        if os.environ.get(self.POSTGRES_ENV_VAR) is not None:
            self.POSTGRES_CONNECTION_STRING = os.environ.get(self.POSTGRES_ENV_VAR)

        self.datastore_builder = DataStoreBuilder()
        self.datastore_builder.set_default_log_level(logging.DEBUG)
        self.datastore_builder.set_print_to_screen(True)
        file_location = self._get_correct_configuration_file()
        if file_location is not None:
            self.datastore_builder.add_file_db(file_location)
        if self.POSTGRES_CONNECTION_STRING is not None:
            self.datastore_builder.add_postgres_db(self.POSTGRES_CONNECTION_STRING)

        self.datastore = self.datastore_builder.build()

        self.logger = self.datastore.get_logger()

        self.manager = None

    def _get_correct_configuration_file(self):
        """Resolve the configuration file if possible."""
        if os.environ.get(self.FILE_LOCATION_ENV_VAR) is not None:
            return os.environ.get(self.FILE_LOCATION_ENV_VAR)

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
        # if self.logger is not None:
        #     self.logger.warning("The config file was not found in the current working directory, ~/ or /etc/.")
        return None

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
            'configuration': self.datastore,
            'plugin_manager': self.manager,
            'logger': self.logger,
            'arguments': args
        }
        return cmd_dictionary

    def init_manager(self):
        self.manager = PluginManager()

        # Commands
        #  Power Commands
        from ..commands.power import PowerCycleCommand, PowerOffCommand, PowerOnCommand
        self.manager.register_plugin_class(PowerCycleCommand)
        self.manager.register_plugin_class(PowerOffCommand)
        self.manager.register_plugin_class(PowerOnCommand)

        #  Resource Commands
        from ..commands.resource_pool import ResourcePoolCheckCommand, ResourcePoolAddCommand, ResourcePoolRemoveCommand
        self.manager.register_plugin_class(ResourcePoolCheckCommand)
        self.manager.register_plugin_class(ResourcePoolAddCommand)
        self.manager.register_plugin_class(ResourcePoolRemoveCommand)

        #  Service Commands
        from ..commands.services import ServicesStartCommand, ServicesStatusCommand, ServicesStopCommand
        self.manager.register_plugin_class(ServicesStartCommand)
        self.manager.register_plugin_class(ServicesStatusCommand)
        self.manager.register_plugin_class(ServicesStopCommand)

        #  BIOS Commands
        from ..commands.bios import BiosUpdateCommand, BiosVersionCommand
        self.manager.register_plugin_class(BiosUpdateCommand)
        self.manager.register_plugin_class(BiosVersionCommand)

        # BMC Plugins
        from ..bmc import BmcIpmiUtil, BmcMock
        self.manager.register_plugin_class(BmcIpmiUtil)
        self.manager.register_plugin_class(BmcMock)

        # os remote access plugins
        from ..os_remote_access import RemoteSshPlugin, RemoteTelnetPlugin, OsRemoteAccessMock
        self.manager.register_plugin_class(RemoteSshPlugin)
        self.manager.register_plugin_class(RemoteTelnetPlugin)
        self.manager.register_plugin_class(OsRemoteAccessMock)

        # pdu plugins
        from ..pdu import PduIPS400, PduRaritanPX35180CR, PduMock
        self.manager.register_plugin_class(PduIPS400)
        self.manager.register_plugin_class(PduRaritanPX35180CR)
        self.manager.register_plugin_class(PduMock)

        # power control plugins
        from ..power_control import NodePower, PowerControlMock
        self.manager.register_plugin_class(NodePower)
        self.manager.register_plugin_class(PowerControlMock)

        # Resource Manager Plugins
        from ..resource import SlurmResource, MockResource
        self.manager.register_plugin_class(SlurmResource)
        self.manager.register_plugin_class(MockResource)

        # NodeController Plugins for BIOS
        from ..bios import MockNC
        self.manager.register_plugin_class(MockNC)

        from ..commands.provisioner import ProvisionerDeleteCommand, ProvisionerAddCommand, ProvisionerSetCommand
        self.manager.register_plugin_class(ProvisionerAddCommand)
        self.manager.register_plugin_class(ProvisionerDeleteCommand)
        self.manager.register_plugin_class(ProvisionerSetCommand)

        from ..provisioner import MockProvisioner, Warewulf
        self.manager.register_plugin_class(MockProvisioner)
        self.manager.register_plugin_class(Warewulf)

        try:
            from ctrl_plugins import add_plugins_to_manager
            add_plugins_to_manager(self.manager)
        except ImportError:
            pass

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
                       'service_stop': 'service_stop',
                       'bios_update': 'bios_update',
                       'bios_version': 'bios_version',
                       'provisioner_add': 'provisioner_add',
                       'provisioner_delete': 'provisioner_delete',
                       'provisioner_set': 'provisioner_set'
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
            cmd_obj = self.manager.create_instance('command', command_map[sub_command], cmd_dictionary)
            self.logger.journal(cmd_obj.get_name(), cmd_obj.command_args, device)
            command_result = cmd_obj.execute()

            command_result.device_name = device
            self.logger.journal(cmd_obj.get_name(), cmd_obj.command_args, device, command_result)

            results.append(command_result)

        if len(results) == 1:
            return results[0]

        return results

    def device_exists_in_config(self, device_name):
        """Check if the device exists in the configuration file or not"""
        return self.datastore.get_device(device_name) is not None

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

    def get_datastore(self):
        """
        This is not a command, but configuration and node information is stored here and should be acessable from the
        from end. Because DataStore already has a solid API, it doesn't make sense to replicate it here. Instead
        direct access to the DataStore module is given.
        :return: DataStore Module
        """
        return self.datastore

    def bios_update(self, device_name, cmd_args=None):
        """Execute a bios update"""
        return self.common_cmd_invoker(device_name, "bios_update", cmd_args)

    def bios_version(self, device_name, cmd_args=None):
        """Get BIOS version on node"""
        return self.common_cmd_invoker(device_name, "bios_version", cmd_args)

    def provision_add(self, device_name, cmd_args=None):
        return self.common_cmd_invoker(device_name, "provisioner_add", cmd_args)

    def provision_delete(self, device_name, cmd_args=None):
        return self.common_cmd_invoker(device_name, "provisioner_delete", cmd_args)

    def provision_set(self, device_name, cmd_args=None):
        return self.common_cmd_invoker(device_name, "provisioner_set", cmd_args)
