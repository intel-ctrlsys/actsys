# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
ServicesCheckCommand Plugin
"""
from .. import Command, CommandResult
from ...utilities.remote_access_data import RemoteAccessData


class ServicesCommand(Command):
    """ServicesCheckCommand"""

    SSH_CONNECTION_ERROR = 255
    SSH_RETRIES = 1
    SSH_SUCCESS = 0

    def __init__(self, device_name, configuration, plugin_manager, logger=None):
        """Retrieve dependencies and prepare for power on"""
        Command.__init__(self, device_name, configuration, plugin_manager, logger)
        self.command = []

    def execute(self):
        """Execute the command"""
        try:
            assert self.command is not []
            result_list = []
            remote_access_list = []
            ipaddress_hostname_dict = {}

            for device in self.device_name:
                device = self.configuration.get_device(device)
                remote_access_list.append(RemoteAccessData(device.get("ip_address"), device.get("port"),
                                                           device.get("user"), device.get("password")))
                ipaddress_hostname_dict[device.get("ip_address")] = device.get("hostname")

            device = self.configuration.get_device(self.device_name[0])
            ssh = self.plugin_manager.create_instance('os_remote_access', device.get("access_type"))
            service_list = device.get("service_list", [])
            for service in service_list:
                self.logger.debug("Attempting to check for service {} on nodes {}".format(service,
                                                                                          self.device_name))
                self.command.append(service)
                ssh_result = ssh.execute_multiple_nodes(list(self.command), remote_access_list, True)
                self.command.pop()

                for key, value in list(ssh_result.items()):
                    result_string = str(value)
                    cmd_result = CommandResult(value.return_code, result_string)
                    cmd_result.device_name = ipaddress_hostname_dict[key]
                    result_list.append(cmd_result)

            if not service_list:
                self.logger.info("No services were specified in the configuration file for {}. "
                                 "Was this intended?".format(device.get("device_id")))
                result_string = 'Success: no services checked'
                result_list.append(CommandResult(0, result_string))
            return result_list
        except RuntimeError as err:
            return [CommandResult(message=str(err))]
