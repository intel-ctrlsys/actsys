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

    def __init__(self, args=None):
        """Retrieve dependencies"""
        BiosCommand.__init__(self, args)

    def execute(self):
        """Execute the command"""
        self.setup()
        if self.args.image is None:
            return CommandResult(255, "Please provide BIOS image. See usage")
        try:
            ret_msg = self.node_controller.bios_update(self.device_name, self.args.image)
        except Exception as ex:
            return CommandResult(255, ex.message)
        return CommandResult(0, ret_msg)
