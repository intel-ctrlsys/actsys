# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
ServicesCheckCommand Plugin
"""
from ...plugin import DeclarePlugin
from .services import ServicesCommand


@DeclarePlugin('service_start', 100)
class ServicesStartCommand(ServicesCommand):
    """ServicesCheckCommand"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None):
        """Retrieve dependencies and prepare for power on"""
        ServicesCommand.__init__(self, device_name, configuration, plugin_manager, logger)
        self.command = ["systemctl", "start"]
