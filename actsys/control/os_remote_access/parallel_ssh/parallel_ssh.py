# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Implements the remote access contract using ssh for remote access to the OS on
a compute node.
"""
from pssh.pssh_client import ParallelSSHClient
from ...utilities.utilities import Utilities, SubprocessOutput
from ..os_remote_access import OsRemoteAccess
from ...plugin import DeclarePlugin


@DeclarePlugin('parallel_ssh', 100)
class ParallelSshPlugin(OsRemoteAccess):
    """SSH remote OS access implementation."""

    def __init__(self, connect_timeout=4):
        OsRemoteAccess.__init__(self)
        self.__connect_timeout = connect_timeout
        self.utilities = Utilities()

    def execute_multiple_nodes(self, cmd, remote_access_list, capture=False, other=None):
        """Execute the remote command on multiple nodes in parallel"""
        client = self._get_parallel_ssh_client(remote_access_list)
        str_cmd = ' '.join(cmd)
        output = client.run_command(str_cmd, stop_on_errors=False)
        client.join(output)
        return self._process_output(output, cmd)

    @classmethod
    def _get_parallel_ssh_client(cls, remote_access_list):
        """Make the ssh command"""
        target = []
        for remote_access_data in remote_access_list:
            target.append(str(remote_access_data.address))
        client = ParallelSSHClient(target)
        return client

    @classmethod
    def _process_output(cls, output, cmd):
        result = {}
        if output is None:
            raise RuntimeError("Failed to run command in parallel")
        for host, host_output in output.items():
            host_stdout = ""
            host_stderr = ""
            if host_output.exit_code == 0:
                host_stdout = "Success: {} - {}".format(cmd[1], cmd[2])
            else:
                for line in host_output.stdout:
                    host_stderr += "{}\n".format(str(line.encode('utf-8')))
                for line in host_output.stderr:
                    host_stderr += "{}\n".format(str(line.encode('utf-8')))
                if host_output.exception:
                    host_stderr += "{}\n".format(str(host_output.exception.encode('utf-8')))
            result[host] = SubprocessOutput(host_output.exit_code, host_stdout, host_stderr)
        return result
