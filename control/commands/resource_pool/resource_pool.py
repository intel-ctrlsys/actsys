# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Add Plugin
"""
from ..command import Command, CommandResult


class ResourcePoolCommand(Command):
    """ResourcePoolAddCommand"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None):
        """Retrieve dependencies and prepare for power on"""
        Command.__init__(self, device_name, configuration, plugin_manager, logger)
        self.device = None
        self.resource_manager = None

    def setup(self):
        """Setup for the command"""

        self.device = self.configuration.get_device(self.device_name)
        if 'compute' != self.device.get("device_type") and 'node' != self.device.get("device_type"):
            return CommandResult(-1, "The device is not a compute node!")
        self.resource_manager = self.plugin_manager.create_instance('resource_control',
                                                                    self.device.get("resource_controller"))
        if not self.resource_manager.check_resource_manager_installed():
            return CommandResult(-2, "Resource manager is not installed!")

        return None
