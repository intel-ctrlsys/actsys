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
        self.resource_manager = None

    def setup(self):
        """
        Setup for the command.

        :return:
        :raise: ConfigurationNeeded Exception if the config has not been set probperly
        """
        for device_list_item in self.device_name:
            device = self.configuration.get_device(device_list_item)
            if device.get("device_type") != 'compute' and \
               device.get("device_type") != 'node':
                return CommandResult(-1, "The device " + device_list_item +
                                     " is not a compute node!")

            resource_controller = device.get("resource_controller")

            if resource_controller is None:
                return CommandResult(0, "The resource manager for device " +
                                     device_list_item + " is not specified!")

            if self.resource_manager is None:
                try:
                    self.resource_manager = self.plugin_manager.create_instance(
                        'resource_control', resource_controller)
                except:
                    raise ConfigurationNeeded("resource_controller",
                                              device_list_item,
                                              self.plugin_manager.
                                              get_sorted_plugins_for_framework
                                              ("resource_control"))

        if not self.resource_manager.check_resource_manager_running():
            return CommandResult(-2, "Resource manager is not running!")

        return None
