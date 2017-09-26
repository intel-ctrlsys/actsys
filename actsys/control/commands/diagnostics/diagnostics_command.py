# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Diagnostics inband Plugin
"""
from .. import Command


class DiagnosticsCommand(Command):
    """"Diagnostics command interfaces"""""
    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        Command.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)
        self.plugin_name = None
        self.plugin_manager = plugin_manager
        self.device = None
        self.diagnostics_plugin = None
        self.diags_plugin_type = None
        self.bmc_data = None
        self.options = kwargs
        self.options['plugin_manager'] = self.plugin_manager

    def setup(self):
        """Setup function to setup for diagnostics command"""
        self.device = self.configuration.get_device(self.device_name[0])
        if self.device.get("device_type") not in ['node', 'compute', 'service']:
            raise RuntimeError('Cannot run diagnostics on a non-node type '
                               'device!')
        self.bmc_data = self.configuration.get_device(self.device.get("bmc"))
        self.diags_plugin_type = self.device.get("diagnostics", None)
        self.diagnostics_plugin = self.plugin_manager.create_instance('diagnostics', self.diags_plugin_type,
                                                                      **self.options)
        return None
