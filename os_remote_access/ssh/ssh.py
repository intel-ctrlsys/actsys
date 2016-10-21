# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements the remote access contract using ssh for remote access to the OS on
a compute node.
"""
from ctrl.utilities.utilities import Utilities
from ctrl.os_remote_access.os_remote_access import OsRemoteAccess
from ctrl.plugin.manager import PluginMetadataInterface


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        PluginMetadataInterface.__init__(self)

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
        OsRemoteAccess.__init__(self, options)
        self.__options = options
        self.utilities = Utilities()

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Execute the remote command"""
        if capture:
            return self._execute_ssh_with_capture(cmd, remote_access_data)
        else:
            return self._execute_ssh(cmd, remote_access_data)

    @classmethod
    def _build_command(cls, command, remote_access_data):
        """Make the ssh command"""
        platform = ['ssh', '-I', '-p', '-q']
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
        cmd = [platform[0], platform[3]] + id_file + port_opt + [target]
        cmd = cmd + command
        return cmd

    def _execute_ssh(self, cmdargs, remote_access_data):
        """Execute command on the remote server returning the result"""
        full_command = RemoteSshPlugin._build_command(cmdargs,
                                                      remote_access_data)
        return self.utilities.execute_no_capture(full_command), None

    def _execute_ssh_with_capture(self, command, remote_access_data):
        """Execute command on the remote server returning the result and
           output"""
        full_command = RemoteSshPlugin._build_command(command,
                                                      remote_access_data)
        result = self.utilities.execute_with_capture(full_command)
        if result is None:
            return 255, None
        else:
            return 0, result
