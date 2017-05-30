# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
BIOS Commands
"""
from ..command import Command, CommandResult


class BiosCommand(Command):
    """Update BIOS firmware on node"""
    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        Command.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)
        self.device = None
        self.bmc = None
        self.node_controller = None

    def setup(self):
        """Setup for Bios Commands"""
        self.device = self.configuration.get_device(self.device_name)
        self.bmc = self.configuration.get_device(self.device.get('bmc'))
        device_type = self.device.get("device_type")
        bios_controller = self.device.get("bios_controller")
        if device_type not in ['compute', 'node']:
            return CommandResult(255, "The device is not a compute node!")
        if bios_controller is None:
            return CommandResult(255, "Please provide bios controller type in configuration")
        self.node_controller = self.plugin_manager.create_instance('bmc', bios_controller)
        return None
