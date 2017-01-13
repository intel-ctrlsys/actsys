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
from ...plugin import DeclarePlugin

# timeout parameter (estimated 10s) specifies timeout in seconds
# for blocking connection attempt operation (default 4 m)
TIMEOUT = 10
SLEEP_TIME = TIMEOUT + 1


@DeclarePlugin('telnet', 100)
class RemoteTelnetPlugin(OsRemoteAccess):
    """Telnet remote OS access implementation."""
    def __init__(self, options=None):
        OsRemoteAccess.__init__(self, options)

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
            # print "Telnet: Error connecting to remote device"
            return None
        if remote_access_data.username != 'None':
            tnet.read_until("login:")
            tnet.write("\r\n" + remote_access_data.username + "\r\n")
        if remote_access_data.identifier != 'None':
            tnet.read_until("Password: ")
            tnet.write("\r\n" + remote_access_data.identifier + "\r\n")
            tnet.read_until(">")
        return tnet
