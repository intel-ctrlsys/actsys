# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Check Plugin
"""
from ..command import Command, CommandResult
from ...plugin.manager import PluginMetadataInterface
from ...resource.slurm.slurm_resource_control import SlurmResource


class PluginMetadata(PluginMetadataInterface):
    """Metadata for this plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'command'

    def name(self):
        """Get the plugin instance name."""
        return 'resource_pool_check'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return ResourcePoolCheckCommand(options)


class ResourcePoolCheckCommand(Command):
    """ResourcePoolCheckCommand"""

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ResourcePoolCheckCommand, self).__init__(args)

    def execute(self):
        """Execute the command"""
        device = self.configuration.get_device(self.device_name)
        if 'compute' != device.device_type and 'node' != device.device_type:
            return CommandResult(-1, "The device is not a compute node!")
        sr = SlurmResource()
        if not sr.check_resource_manager_installed():
            return CommandResult(-2, "Slurm resource manager is not installed!")

        rc, message = sr.check_node_state(self.device_name)
        return CommandResult(rc, message)
