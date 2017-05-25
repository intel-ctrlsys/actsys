# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Diagnostics online Plugin
"""
from .. import CommandResult, Command
from control.plugin import DeclarePlugin
from .diagnostics_command import DiagnosticsCommand


@DeclarePlugin('diagnostics_offline', 100)
class DiagnosticsOfflineCommand(DiagnosticsCommand):
    """DiagnosticsOnline"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        DiagnosticsCommand.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)

    def execute(self):
        """Execute the command"""
        return CommandResult(0, 'Diagnostics offline: Plugin not implemented')
