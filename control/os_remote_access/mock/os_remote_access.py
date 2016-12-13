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
from ...plugin.manager import PluginMetadataInterface
import json
import os


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'os_remote_access'

    def name(self):
        """Get the plugin instance name."""
        return 'mock'

    def priority(self):
        """Get the priority of this name in this category."""
        return 1000

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return OsRemoteAccessMock(options)


class OsRemoteAccessMock(OsRemoteAccess):
    """SSH remote OS access implementation."""
    def __init__(self, options=None):
        super(OsRemoteAccessMock, self).__init__(options)
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
