# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements the remote access contract using a mock for remote access to the OS
on a compute node.
"""
from ...utilities.utilities import Utilities
from ..os_remote_access import OsRemoteAccess
from ...plugin import DeclarePlugin
import json
import os


@DeclarePlugin('mock', 1000)
class OsRemoteAccessMock(OsRemoteAccess):
    """SSH remote OS access implementation."""
    def __init__(self, options=None):
        OsRemoteAccess.__init__(self, options)
        self.__options = options
        self.utilities = Utilities()
        self.dfx_result_list = []
        self._load_test_results()

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Execute the remote command"""
        if capture:
            return 0, ''
        else:
            return 0, None

    def test_connection(self, remote_access_data):
        """Execute the remote command"""
        if len(self.dfx_result_list) == 0:
            return False
        else:
            rv = self.dfx_result_list[0]
            self.dfx_result_list = self.dfx_result_list[1:]
            return rv

    def _load_test_results(self):
        filename = os.path.join(os.path.sep, 'tmp', 'mock_os_test_results')
        try:
            file_desc = open(filename, 'r')
            self.dfx_result_list = json.load(file_desc)
            file_desc.close()
        except IOError:
            pass
