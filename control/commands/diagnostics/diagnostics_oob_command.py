# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Diagnostics inband Plugin
"""
from .. import CommandResult, Command
from control.plugin import DeclarePlugin
from .diagnostics_command import DiagnosticsCommand


@DeclarePlugin('diagnostics_oob', 100)
class DiagnosticsOOBCommand(DiagnosticsCommand):
    """Diagnosticsinband"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        DiagnosticsCommand.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)

    def execute(self):
        """Execute the command"""
        return CommandResult(0, 'Diagnostics Out of Band: Plugin not implemented')
