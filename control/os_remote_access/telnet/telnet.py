# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements the remote access contract using telnet
"""

import telnetlib
import time
from ..os_remote_access import OsRemoteAccess
from ...plugin.manager import PluginMetadataInterface

# timeout parameter (estimated 10s) specifies timeout in seconds
# for blocking connection attempt operation (default 4 m)
TIMEOUT = 10
SLEEP_TIME = TIMEOUT + 1

class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'os_remote_access'

    def name(self):
        """Get the plugin instance name."""
        return 'telnet'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return RemoteTelnetPlugin(options)


class RemoteTelnetPlugin(OsRemoteAccess):
    """Telnet remote OS access implementation."""
    def __init__(self, options=None):
        super(RemoteTelnetPlugin, self).__init__(options)

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Execute the remote command"""
        tnet = self._establish_connection(remote_access_data)
        result = None
        if tnet is not None:
            tnet.write("\r" + cmd + "\r\n")
            tnet.read_until(">")
            result = tnet.read_until(">")
            tnet.close()
        return result

    def test_connection(self, remote_access_data):
        raise NotImplementedError('RemoteTelnetPlugin.test_connection is not '
                                  'implemented!')

    @classmethod
    def _establish_connection(cls, remote_access_data):
        """Establish telnet connection"""
        try:
            time.sleep(SLEEP_TIME)
            tnet = telnetlib.Telnet(remote_access_data.address, timeout=TIMEOUT)
        except EnvironmentError:
            print "Telnet: Error connecting to remote device"
            return None
        if remote_access_data.username != 'None':
            tnet.read_until("login:")
            tnet.write("\r\n" + remote_access_data.username + "\r\n")
        if remote_access_data.identifier != 'None':
            tnet.read_until("Password: ")
            tnet.write("\r\n" + remote_access_data.identifier + "\r\n")
            tnet.read_until(">")
        return tnet
