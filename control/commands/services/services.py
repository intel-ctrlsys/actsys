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
        assert self.command is not []
        result_list = []

        for device in self.device_name:

            device = self.configuration.get_device(device)
            remote_access_data = RemoteAccessData(device.get("ip_address"), device.get("port"),
                                                  device.get("user"), device.get("password"))
            ssh = self.plugin_manager.create_instance('os_remote_access', device.get("access_type"))
            hostname = device['hostname']
            if device.get("device_type") not in ['compute', 'node']:
                command_result = CommandResult(1, '{}: Failure: cannot perform service actions this device '
                                                  'type ({})'.format(hostname, device.get("device_type")))
                result_list.append(command_result)

            result_retries = 1
            result_string = ""
            result_msg = ""
            result_code = 0

            service_list = device.get("service_list", [])
            for service in service_list:
                self.logger.debug("Attempting to check for service {} on node {}".format(service,
                                                                                         device.get("device_id")))

                self.command.append(service)
                ssh_result = ssh.execute(list(self.command), remote_access_data, True)
                self.command.pop()

                if ssh_result.return_code == self.SSH_CONNECTION_ERROR and result_retries < self.SSH_RETRIES:
                    self.logger.debug("Failed to connect over SSH, retrying...")
                    service_list.append(service)
                    result_retries += 1
                    continue
                elif ssh_result.return_code != self.SSH_SUCCESS:
                    result_msg = "{}: Failed: {} - {}".format(hostname, self.command[1], service)
                    if ssh_result.stdout is not None:
                        result_msg += "\n {}".format(ssh_result.stdout)
                    result_code = 1
                else:
                    result_msg = "{}: Success: {} - {}".format(hostname, self.command[1], service)

                cr = CommandResult(ssh_result.return_code, result_msg)
                result_string += str(cr) + '\n'

            if result_string == '':
                self.logger.info("No services were specified in the configuration file for {}. "
                                 "Was this intended?".format(device.get("device_id")))
                result_string = 'Success: no services checked'

            command_result = CommandResult(result_code, result_string.rstrip('\n'))
            result_list.append(command_result)
        return result_list
