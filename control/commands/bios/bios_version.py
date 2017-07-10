# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
 Get BIOS version
"""
from ...commands.command import CommandResult
from ...plugin import DeclarePlugin
from .bios import BiosCommand


@DeclarePlugin('bios_version', 100)
class BiosVersionCommand(BiosCommand):
    """Bios Get Version Command"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None):
        """Retrieve dependencies and prepare for power on"""
        BiosCommand.__init__(self, device_name, configuration, plugin_manager, logger)

    def execute(self):
        """Execute the command"""
        try:
            self.setup()
            result = []
            result_dict = self.node_controller.get_version(self.device_data, self.bmc_data)
            for key, value in result_dict.iteritems():
                command_result = CommandResult(0, value)
                command_result.device_name = key
                result.append(command_result)
        except Exception as ex:
            return [CommandResult(255, ex.message)]
        return result
