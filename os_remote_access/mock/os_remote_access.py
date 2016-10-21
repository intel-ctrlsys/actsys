# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements the remote access contract using a mock for remote access to the OS
on a compute node.
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
        OsRemoteAccess.__init__(self)
        self.__options = options
        self.utilities = Utilities()

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Execute the remote command"""
        if capture:
            return 0, ''
        else:
            return 0, None
