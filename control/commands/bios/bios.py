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
        self.device_data = []
        self.bmc_data = []
        self.node_controller = None

    def setup(self):
        """Setup for Bios Commands"""
        for device in self.device_name:
            node = self.configuration.get_device(device)
            if node.get("device_type") not in ['node', 'compute', 'service']:
                raise RuntimeError('Sensor values can not be read for a non-node type '
                                   'device!')
            self.device_data.append(node)
            self.bmc_data.append(self.configuration.get_device(node.get("bmc")))
        bios_controller = self.bmc_data[0].get("access_type", None)
        if bios_controller is None:
            raise RuntimeError("No BMC access_type specified in the configuration file. Cannot perform action")
        self.node_controller = self.plugin_manager.create_instance('bmc', bios_controller)
