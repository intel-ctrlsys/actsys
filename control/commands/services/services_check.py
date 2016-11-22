# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
ServicesCheckCommand Plugin
"""
from .. import Command, CommandResult
from ...plugin.manager import PluginMetadataInterface
from ...utilities.remote_access_data import RemoteAccessData


class PluginMetadata(PluginMetadataInterface):
    """Metadata for this plugin."""

    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'command'

    def name(self):
        """Get the plugin instance name."""
        return 'service_check'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return ServicesCheckCommand(options)


class ServicesCheckCommand(Command):
    """ServicesCheckCommand"""

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ServicesCheckCommand, self).__init__(args)

        self.device = self.configuration.get_device(self.device_name)
        self.ssh = self.plugin_manager.factory_create_instance(
            'os_remote_access', 'ssh')
        self.remoteAccessData = RemoteAccessData(self.device.ip_address, self.device.port,
                                                 self.device.user, self.device.password)

    def execute(self):
        """Execute the command"""
        if self.device.device_type != 'compute':
            return CommandResult(1, 'Failure: cannot check services this device'
                                    ' type {}'.format(self.device.device_type))

        failed_results = []

        for service in self.device.service_list:
            cmd = 'systemctrl status {}'.format(service)
            ssh_result = self.ssh.execute(cmd, self.remoteAccessData)
            if ssh_result.code != 0:
                result_string = "Failed: {} service was not active.".format(service)
                failed_results.append(
                    CommandResult(ssh_result.code, result_string))

        if len(failed_results) == 0:
            return CommandResult(0, "Success: All services running for {}".
                                 format(self.device_name))
        else:
            result_string = ""
            for res in failed_results:
                result_string += str(res)
            return CommandResult(1, result_string)
