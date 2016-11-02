# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Remove Plugin
"""
from ctrl.commands import Command, CommandResult
from ctrl.plugin.manager import PluginMetadataInterface


class PluginMetadata(PluginMetadataInterface):
    """Metadata for this plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'command'

    def name(self):
        """Get the plugin instance name."""
        return 'resource_pool_remove'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return ResourcePoolRemoveCommand(options)


class ResourcePoolRemoveCommand(Command):
    """ResourcePoolRemoveCommand"""

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ResourcePoolRemoveCommand, self).__init__(args)

    def execute(self):
        """Execute the command"""
        return CommandResult(0, "Success: Resource Pool Remove {}".
                             format(self.device_name))
