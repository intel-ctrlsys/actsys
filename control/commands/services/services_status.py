# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
ServicesCheckCommand Plugin
"""
from ...plugin.manager import PluginMetadataInterface
from .services import ServicesCommand


class PluginMetadata(PluginMetadataInterface):
    """Metadata for this plugin."""

    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'command'

    def name(self):
        """Get the plugin instance name."""
        return 'service_status'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return ServicesStatusCommand(options)


class ServicesStatusCommand(ServicesCommand):
    """ServicesCheckCommand"""

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ServicesStatusCommand, self).__init__(args)
        self.command = ["systemctl", "status"]
