# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements the remote access contract using ssh for remote access to the OS on
a compute node.
"""
from ...utilities.utilities import Utilities
from ..os_remote_access import OsRemoteAccess
from ...plugin.manager import PluginMetadataInterface


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'os_remote_access'

    def name(self):
        """Get the plugin instance name."""
        return 'ssh'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return RemoteSshPlugin(options)


class RemoteSshPlugin(OsRemoteAccess):
    """SSH remote OS access implementation."""

    def __init__(self, options=None):
        super(RemoteSshPlugin, self).__init__(options)
        self.__connect_timeout = 6
        self.__options = options
        if self.__options is not None and 'ConnectTimeout' in self.__options:
            self.__connect_timeout = self.__options['ConnectTimeout']
        self.utilities = Utilities()

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Execute the remote command"""
        if capture:
            return self._execute_ssh_with_capture(cmd, remote_access_data)
        else:
            return self._execute_ssh(cmd, remote_access_data)

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
        return self.utilities.execute_no_capture(full_command), None

    def _execute_ssh_with_capture(self, command, remote_access_data):
        """Execute command on the remote server returning the result and
           output"""
        full_command = self._build_command(command, remote_access_data)
        stdout, stderr = self.utilities.execute_with_capture(full_command)
        if stdout is None:
            return 255, None
        else:
            return 0, stdout
