# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Implements the remote access contract using a mock for remote access to the OS
on a compute node.
"""
import json
import os
from ...utilities.utilities import SubprocessOutput
from ..os_remote_access import OsRemoteAccess
from ...plugin import DeclarePlugin


@DeclarePlugin('mock', 1000)
class OsRemoteAccessMock(OsRemoteAccess):
    """SSH remote OS access implementation."""
    def __init__(self):
        OsRemoteAccess.__init__(self)
        self.dfx_result_list = []
        self._load_test_results()

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Execute the remote command"""
        if capture:
            output = SubprocessOutput(0, '', '')
        else:
            output = SubprocessOutput(0, None, None)
        return output

    def execute_multiple_nodes(self, cmd, remote_access_list, capture=False, other=None):
        """Execute the remote command on multiple nodes"""
        result = {}
        for remote_access_data in remote_access_list:
            ssh_result = self.execute(cmd, remote_access_data, capture, other)
            result[remote_access_data.address] = ssh_result
        return result

    def test_connection(self, remote_access_data):
        """Execute the remote command"""
        if len(self.dfx_result_list) == 0:
            ret_value = False
        else:
            ret_value = self.dfx_result_list[0]
            self.dfx_result_list = self.dfx_result_list[1:]
        return ret_value

    def _load_test_results(self):
        filename = os.path.join(os.path.sep, 'tmp', 'mock_os_test_results')
        try:
            file_desc = open(filename, 'r')
            self.dfx_result_list = json.load(file_desc)
            file_desc.close()
        except IOError:
            pass
