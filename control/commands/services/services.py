# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
ServicesCheckCommand Plugin
"""
from .. import Command, CommandResult
from ...utilities.remote_access_data import RemoteAccessData


class ServicesCommand(Command):
    """ServicesCheckCommand"""

    SSH_CONNECTION_ERROR = 255
    SSH_RETRIES = 3
    SSH_SUCCESS = 0

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ServicesCommand, self).__init__(args)

        self.device = self.configuration.get_device(self.device_name)
        self.ssh = self.plugin_manager.factory_create_instance('os_remote_access', 'ssh')
        self.remote_access_data = RemoteAccessData(self.device.ip_address, self.device.port,
                                                   self.device.user, self.device.password)
        self.command = []

    def execute(self):
        """Execute the command"""
        assert self.command is not []

        if self.device.device_type not in ['compute', 'node']:
            return CommandResult(1, 'Failure: cannot perform service actions this device'
                                    ' type ({})'.format(self.device.device_type))

        result_retries = 1
        result_string = ""
        result_msg = ""
        result_code = 0
        for service in self.device.service_list:
            self.logger.debug("Attempting to check for service {} on node {}".format(service, self.device.device_id))

            self.command.append(service)
            ssh_result = self.ssh.execute(list(self.command), self.remote_access_data, True)
            self.command.pop()

            if ssh_result[0] == self.SSH_CONNECTION_ERROR and result_retries < self.SSH_RETRIES:
                self.logger.debug("Failed to connect over SSH, retrying...")
                self.device.service_list.append(service)
                result_retries += 1
                continue
            elif ssh_result[0] != self.SSH_SUCCESS:
                result_msg = "Failed: {} - {}".format(self.command[1], service)
                if ssh_result[1] is not None:
                    result_msg += "\n {}".format(ssh_result[1])
                result_code = 1
            else:
                result_msg = "Success: {} - {}".format(self.command[1], service)

            cr = CommandResult(ssh_result[0], result_msg)
            result_string += str(cr) + '\n'

        if result_string == '':
            self.logger.info("No services were specified in the configuration file for {}. "
                             "Was this intended?".format(self.device.device_id))
            result_string = 'Success: no services checked'

        return CommandResult(result_code, result_string.rstrip('\n'))
