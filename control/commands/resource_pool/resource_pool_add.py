# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Add Plugin
"""
from control.commands.command import CommandResult
from control.plugin import DeclarePlugin
from .resource_pool import ResourcePoolCommand


@DeclarePlugin('resource_pool_add', 100)
class ResourcePoolAddCommand(ResourcePoolCommand):
    """ResourcePoolAddCommand"""

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        ResourcePoolCommand.__init__(self, args)

    def execute(self):
        """Execute the command"""

        setup_results = self.setup()
        if setup_results is not None:
            return setup_results

        rc, message = self.resource_manager.add_node_to_resource_pool(self.device_name)
        return CommandResult(rc, message)