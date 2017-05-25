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


@DeclarePlugin('diagnostics_online', 100)
class DiagnosticsOnlineCommand(DiagnosticsCommand):
    """DiagnosticsOnline"""
    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        DiagnosticsCommand.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)

    def execute(self):
        """Execute the command"""
        self.setup()
        try:
            ret_msg = self.diagnostics_plugin.launch_diags(self.device, self.bmc_data)
        except Exception as ex:
                return CommandResult(1, ex.message)
        return CommandResult(0, ret_msg)
