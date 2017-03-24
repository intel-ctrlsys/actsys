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

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        BiosCommand.__init__(self, args)

    def execute(self):
        """Execute the command"""
        self.setup()
        try:
            ret_msg = self.node_controller.get_version(self.device, self.bmc)
        except Exception as ex:
            return CommandResult(255, ex.message)
        return CommandResult(0, ret_msg)
