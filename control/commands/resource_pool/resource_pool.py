# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Resource Pool Add Plugin
"""
from ..command import Command, CommandResult, ConfigurationNeeded


class ResourcePoolCommand(Command):
    """ResourcePoolAddCommand"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None):
        """Retrieve dependencies and prepare for power on"""
        Command.__init__(self, device_name, configuration, plugin_manager, logger)
        self.device = None
        self.resource_manager = None

    def setup(self):
        """
        Setup for the command.

        :return:
        :raise: ConfigurationNeeded Exception if the config has not been set probperly
        """

        self.device = self.configuration.get_device(self.device_name)
        if 'compute' != self.device.get("device_type") and 'node' != self.device.get("device_type"):
            return CommandResult(-1, "The device is not a compute node!")

        resource_controller = self.device.get("resource_controller")

        if resource_controller is None:
            return CommandResult(0, "The resource manager is not specified, nothing to do.")

        try:
            self.resource_manager = self.plugin_manager.create_instance('resource_control', resource_controller)
        except:
            raise ConfigurationNeeded("resource_controller", self.device_name,
                                      self.plugin_manager.get_sorted_plugins_for_framework("resource_control"))

        if not self.resource_manager.check_resource_manager_installed():
            return CommandResult(-2, "Resource manager is not installed!")

        return None
