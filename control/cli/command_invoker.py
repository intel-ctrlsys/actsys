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
import logging
from ..plugin.manager import PluginManager
from ..commands import CommandResult
from datastore import DataStoreBuilder


class CommandInvoker(object):
    """This class contains all the functions exposed to cli code"""

    CTRL_CONFIG_LOCATION = "/usr/share/ctrl_db"
    POSTGRES_ENV_VAR = "CTRL_POSTGRES_CONNECTION_STRING"
    FILE_LOCATION_ENV_VAR = "CTRL_CONFIG_FILE"
    POSTGRES_CONNECTION_STRING = None

    def __init__(self, screen_log_level=logging.WARNING):
        """

        :param log_level: An appropriate log level from the python logging module. This level will be used when
            deciding what to print to the screen. If set to None, then nothing will be printed
        """
        self.invoker_ret_val = 0
        self.failed_device_name = list()

        datastore_location = self.get_config_file_location()
        self.datastore = DataStoreBuilder.get_datastore_from_string(datastore_location, screen_log_level)

        self.logger = self.datastore.get_logger()

        self.manager = None

    @classmethod
    def get_config_file_location(cls):
        return os.environ.get(cls.POSTGRES_ENV_VAR, None) or \
                             os.environ.get(cls.FILE_LOCATION_ENV_VAR, None) or \
                             cls.CTRL_CONFIG_LOCATION

    def _device_name_check(self, device_name):
        """Check the device name & create a list"""
        return self.datastore.expand_device_list(device_name)

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
        from ..power_control import NodePower, PowerControlMock, RestPower
        self.manager.register_plugin_class(NodePower)
        self.manager.register_plugin_class(RestPower)
        self.manager.register_plugin_class(PowerControlMock)

        # Resource Manager Plugins
        from ..resource import SlurmResource, MockResource
        self.manager.register_plugin_class(SlurmResource)
        self.manager.register_plugin_class(MockResource)

        from ..commands.provisioner import ProvisionerDeleteCommand, ProvisionerAddCommand, ProvisionerSetCommand
        self.manager.register_plugin_class(ProvisionerAddCommand)
        self.manager.register_plugin_class(ProvisionerDeleteCommand)
        self.manager.register_plugin_class(ProvisionerSetCommand)

        from ..provisioner import MockProvisioner, Warewulf
        self.manager.register_plugin_class(MockProvisioner)
        self.manager.register_plugin_class(Warewulf)

        from ..commands.oob_sensors import OobSensorGetCommand, OobSensorGetTimeCommand
        self.manager.register_plugin_class(OobSensorGetCommand)
        self.manager.register_plugin_class(OobSensorGetTimeCommand)

        # Diagnostics plugin
        from ..commands.diagnostics import DiagnosticsInBandCommand, DiagnosticsOOBCommand
        self.manager.register_plugin_class(DiagnosticsInBandCommand)
        self.manager.register_plugin_class(DiagnosticsOOBCommand)

        from ..diagnostics.mock_diagnostics.mock_diagnostics import MockDiagnostics
        self.manager.register_plugin_class(MockDiagnostics)

        try:
            from ctrl_plugins import add_plugins_to_manager
            add_plugins_to_manager(self.manager)
        except ImportError as ie:
            self.logger.info("Could not import additional plugins. Proceeding anyways. Err: {}".format(ie))

    def common_cmd_invoker(self, device_regex, sub_command, **kwargs):
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
                       'provisioner_set': 'provisioner_set',
                       'oob_sensor_get': 'oob_sensor_get',
                       'oob_sensor_get_time': 'oob_sensor_get_time',
                       'diagnostics_inband': 'diagnostics_inband',
                       'diagnostics_oob': 'diagnostics_oob'
                       }
        try:
            device_list = self._device_name_check(device_regex)
        except self.datastore.DeviceListParseError as dlpe:
            result = CommandResult(1, "Failed to parse valid device name(s) in {}. Error: {}".format(device_regex, dlpe.message))
            self.logger.warning(result.message)
            return result
        if not device_list:
            return CommandResult(1, "No valid devices to run this command on.")
        results = list()
        valid_node_list = list()
        invalid_node_list = list()
        for device_name in device_list:
            if not self.device_exists_in_config(device_name):
                invalid_node_list.append(device_name)
                continue
            valid_node_list.append(device_name)
            if 'resource' not in sub_command:
                self.create_execute_command(results, device_name,
                                            command_map[sub_command], **kwargs)
        if len(invalid_node_list) > 0:
            node_list = self.datastore.fold_devices(invalid_node_list)
            msg = "Devices {} skipped due to not found in the config file.".\
                format(self.datastore.fold_devices(node_list))
            self.logger.warning(msg)
            results.append(CommandResult(1, msg, node_list))
        if 'resource' in sub_command and len(valid_node_list) > 0:
            devices = self.datastore.fold_devices(valid_node_list)
            self.create_execute_command(results, devices,
                                        command_map[sub_command], **kwargs)
        if len(results) == 1:
            return results[0]

        return results

    def create_execute_command(self, results,
                               devices, sub_command, **kwargs):
        # Prepare kwargs
        kwargs["device_name"] = devices
        kwargs["configuration"] = self.datastore
        kwargs["plugin_manager"] = self.manager
        kwargs["logger"] = self.logger
        # End kwargs prep

        cmd_obj = self.manager.create_instance('command', sub_command, **kwargs)
        self.logger.journal(cmd_obj.get_name(), cmd_obj.command_args, devices)
        try:
            command_result = cmd_obj.execute()
        except Exception as ex:
            command_result = CommandResult(1, ex.message)

        command_result.device_name = devices
        self.logger.journal(cmd_obj.get_name(),
                            cmd_obj.command_args, devices, command_result)

        results.append(command_result)

    def device_exists_in_config(self, device_name):
        """Check if the device exists in the configuration file or not"""
        return self.datastore.get_device(device_name) is not None

    def power_on_invoker(self, device_name, sub_command, force=None, outlet=None):
        """Execute Power On Command"""
        return self.common_cmd_invoker(device_name, sub_command, subcommand=sub_command, force=force, outlet=outlet)

    def power_off_invoker(self, device_name, sub_command, force=None, outlet=None):
        """Execute Power Off Command"""
        return self.common_cmd_invoker(device_name, sub_command, subcommand=sub_command, force=force, outlet=outlet)

    def power_cycle_invoker(self, device_name, sub_command, force=None, outlet=None):
        """Execute Power Reboot Command"""
        return self.common_cmd_invoker(device_name, sub_command, subcommand=sub_command, force=force, outlet=outlet)

    def resource_add(self, device_name):
        """Execute Resource Add Command"""
        return self.common_cmd_invoker(device_name, "resource_add")

    def resource_remove(self, device_name):
        """Execute Resource Add Command"""
        return self.common_cmd_invoker(device_name, "resource_remove")

    def resource_check(self, device_name):
        """Execute Resource Add Command"""
        return self.common_cmd_invoker(device_name, "resource_check")

    def service_status(self, device_name):
        """Execute a service check command"""
        return self.common_cmd_invoker(device_name, "service_status")

    def service_on(self, device_name):
        """Execute a service check command"""
        return self.common_cmd_invoker(device_name, "service_start")

    def service_off(self, device_name):
        """Execute a service check command"""
        return self.common_cmd_invoker(device_name, "service_stop")

    def get_datastore(self):
        """
        This is not a command, but configuration and node information is stored here and should be acessable from the
        from end. Because DataStore already has a solid API, it doesn't make sense to replicate it here. Instead
        direct access to the DataStore module is given.
        :return: DataStore Module
        """
        return self.datastore

    def bios_update(self, device_name, image):
        """Execute a bios update"""
        return self.common_cmd_invoker(device_name, "bios_update", image=image)

    def bios_version(self, device_name):
        """Get BIOS version on node"""
        return self.common_cmd_invoker(device_name, "bios_version")

    def provision_add(self, device_name, provisioner=None):
        """
        Add a device to a provisioner
        :param device_name:
        :param provisioner: The provisioner to add this device too. If nothing is supplied, attempts to add to the
            provisioner specified in the device properties.
        :return: CommandResult
        """
        return self.common_cmd_invoker(device_name, "provisioner_add", provisioner=provisioner)

    def provision_delete(self, device_name):
        """
        Remove a device from the provisioner
        :param device_name:
        :return:
        """
        return self.common_cmd_invoker(device_name, "provisioner_delete")

    def provision_set(self, device_name, ip_address=None, hw_address=None, net_interface=None, image=None,
                      bootstrap=None, files=None, kernel_args=None):
        """
        Set options for a device. The device must already be added to a provisioner. Specify the options you want to set
        or pass in the str("UNDEF") for the options you want to clear.
        :param device_name:
        :param ip_address:
        :param hw_address:
        :param net_interface:
        :param image:
        :param bootstrap:
        :param files:
        :param kernel_args:
        :return:
        """
        return self.common_cmd_invoker(device_name, "provisioner_set", ip_address=ip_address, hw_address=hw_address,
                                       net_interface=net_interface, image=image, bootstrap=bootstrap, files=files,
                                       kernel_args=kernel_args)

    def oob_sensor_get(self, device_name, sensor_name):
        """
        Get the values for a oob sensor
        :param device_name:
        :param sensor_name:
        :return:
        """
        return self.common_cmd_invoker(device_name, "oob_sensor_get", sensor_name=sensor_name)

    def oob_sensor_get_over_time(self, device_name, sensor_name, duration, sample_rate):
        """
        Get the values for a oob sensor
        :param device_name:
        :param sensor_name:
        :param duration:
        :param sample_rate:
        :return:
        """
        return self.common_cmd_invoker(device_name, "oob_sensor_get_time", sensor_name=sensor_name, duration=duration,
                                       sample_rate=sample_rate)

    def diagnostics_inband(self, device_name, test=None, image=None):
        """Execute the inband Diagnostics"""
        return self.common_cmd_invoker(device_name, "diagnostics_inband", test_name=test, diag_image=image)

    def diagnostics_oob(self, device_name, test=None):
        """Execute the oob Diagnostics"""
        return self.common_cmd_invoker(device_name, "diagnostics_oob", test_name=test)

