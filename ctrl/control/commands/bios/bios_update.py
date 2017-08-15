# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
BIOS Flash Plugin
"""
from ...commands.command import CommandResult
from ...plugin import DeclarePlugin
from .bios import BiosCommand


@DeclarePlugin('bios_update', 100)
class BiosUpdateCommand(BiosCommand):
    """Bios Update Command"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, image=None):
        """Retrieve dependencies"""
        BiosCommand.__init__(self, device_name, configuration, plugin_manager, logger, image=image)
        self.image = image

    def execute(self):
        """Execute the command"""
        try:
            self.setup()
            result = []
            if self.image is None:
                return [CommandResult(255, "Please provide BIOS image. See usage")]
            result_dict = self.node_controller.bios_update(self.device_data, self.bmc_data, self.image)
            for key, value in result_dict.iteritems():
                command_result = CommandResult(0, value)
                command_result.device_name = key
                result.append(command_result)
        except Exception as ex:
            return [CommandResult(255, ex.message)]
        return result
