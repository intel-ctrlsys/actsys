# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Remove Plugin
"""
from control.commands.command import CommandResult
from control.plugin.manager import PluginMetadataInterface
from .resource_pool import ResourcePoolCommand


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


class ResourcePoolRemoveCommand(ResourcePoolCommand):
    """ResourcePoolRemoveCommand"""

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ResourcePoolRemoveCommand, self).__init__(args)

    def execute(self):
        """Execute the command"""
        setup_results = self.setup()
        if setup_results is not None:
            return setup_results

        rc, message = self.resource_manager.remove_node_from_resource_pool(self.device_name)
        return CommandResult(rc, message)