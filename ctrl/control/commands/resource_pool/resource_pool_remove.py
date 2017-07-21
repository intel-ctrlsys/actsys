# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Remove Plugin
"""
from control.commands.command import CommandResult
from control.plugin.manager import DeclarePlugin
from .resource_pool import ResourcePoolCommand


@DeclarePlugin('resource_pool_remove', 100)
class ResourcePoolRemoveCommand(ResourcePoolCommand):
    """ResourcePoolRemoveCommand"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None):
        """Retrieve dependencies and prepare for power on"""
        ResourcePoolCommand.__init__(self, device_name, configuration, plugin_manager, logger)

    def execute(self):
        """Execute the command"""
        setup_results = self.setup()
        if setup_results is not None:
            return setup_results

        rc, message = self.resource_manager.remove_nodes_from_resource_pool(self.device_name)
        return CommandResult(rc, message)
