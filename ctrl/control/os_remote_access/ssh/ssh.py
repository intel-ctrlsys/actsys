# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Implements the remote access contract using ssh for remote access to the OS on
a compute node.
"""
from ...utilities.utilities import Utilities, SubprocessOutput
from ..os_remote_access import OsRemoteAccess
from ...plugin import DeclarePlugin


@DeclarePlugin('ssh', 100)
class RemoteSshPlugin(OsRemoteAccess):
    """SSH remote OS access implementation."""
    SSH_CONNECTION_ERROR = 255
    SSH_RETRIES = 1
    SSH_SUCCESS = 0

    def __init__(self, connect_timeout=4):
        OsRemoteAccess.__init__(self)
        self.__connect_timeout = connect_timeout
        self.utilities = Utilities()

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Execute the remote command"""
        if capture:
            return self._execute_ssh_with_capture(cmd, remote_access_data)
        else:
            return self._execute_ssh(cmd, remote_access_data)

    def test_connection(self, remote_access_data):
        """Test for ssh access."""
        return_value = self._execute_ssh(['echo', '-n', '""'], remote_access_data).return_code == 0
        return return_value

    def execute_multiple_nodes(self, cmd, remote_access_list, capture=False, other=None):
        """Execute the remote command on multiple nodes"""
        result = {}
        result_retries = 0
        for remote_access_data in remote_access_list:
            ssh_result = self.execute(cmd, remote_access_data, capture, other)
            if ssh_result.return_code == self.SSH_CONNECTION_ERROR and result_retries < self.SSH_RETRIES:
                remote_access_list.append(remote_access_data)
                result_retries += 1
                continue
            elif ssh_result.return_code != self.SSH_SUCCESS:
                result_msg = "Failed: {} - {}: {}".format(cmd[1], cmd[2], str(ssh_result))
            else:
                result_msg = "Success: {} - {}".format(cmd[1], cmd[2])
            result[remote_access_data.address] = SubprocessOutput(ssh_result.return_code, result_msg, None)
        return result

    def _build_command(self, command, remote_access_data):
        """Make the ssh command"""
        platform = ['ssh', '-i', '-p', '-q']
        target = '%s@%s' % (remote_access_data.username,
                            remote_access_data.address)
        id_file = []
        port_opt = []
        if remote_access_data.identifier is not None:
            id_file.append(platform[1])
            id_file.append(remote_access_data.identifier)
        if remote_access_data.port != 22:
            port_opt.append(platform[2])
            port_opt.append("%d" % remote_access_data.port)
        cmd = [platform[0], platform[3]] + id_file + port_opt + [target] +\
            ['-o', 'ConnectTimeout={}'.format(self.__connect_timeout)]
        cmd = cmd + command
        return cmd

    def _execute_ssh(self, cmdargs, remote_access_data):
        """Execute command on the remote server returning the result"""
        full_command = self._build_command(cmdargs, remote_access_data)
        return SubprocessOutput(self.utilities.execute_no_capture(full_command), None, None)

    def _execute_ssh_with_capture(self, command, remote_access_data):
        """Execute command on the remote server returning the result and
           output"""
        full_command = self._build_command(command, remote_access_data)
        return self.utilities.execute_subprocess(full_command)
