# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
TBD
"""
from ctrl.commands import Command, CommandResult


class ResourcePoolAddCommand(Command):
    """ResourcePoolAddCommand"""

    def __init__(self, node_name, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ResourcePoolAddCommand, self).__init__(node_name, args)

        self.node_name = node_name
        self.args = args

    def execute(self):
        """Execute the command"""
        fmt = "Success: Resource Pool Add {}"
        return CommandResult(0, fmt.format(self.node_name))
