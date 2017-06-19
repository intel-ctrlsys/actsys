# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Check Plugin
"""
from control.commands.command import CommandResult
from control.plugin import DeclarePlugin
from .resource_pool import ResourcePoolCommand


@DeclarePlugin('resource_pool_check', 100)
class ResourcePoolCheckCommand(ResourcePoolCommand):
    """ResourcePoolCheckCommand"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None):
        """Retrieve dependencies and prepare for power on"""
        ResourcePoolCommand.__init__(self, device_name, configuration, plugin_manager, logger)

    def execute(self):
        """Execute the command"""
        setup_results = self.setup()
        if setup_results is not None:
            return setup_results

        rc, message = self.resource_manager.check_nodes_state(self.device_name)
        return CommandResult(rc, message)
