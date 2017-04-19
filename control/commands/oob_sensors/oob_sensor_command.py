# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

from .. import Command


class OobSensorCommand(Command):
    """Oob Sensor Command"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        Command.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)
        self.oob_sensor_plugin = None
        self.plugin_name = None
        self.device_data = None
        self.bmc_data = None

    def setup(self):
        cfg = self.configuration
        node = cfg.get_device(self.device_name)
        if node.get("device_type") not in ['node', 'compute', 'service']:
            raise RuntimeError('Sensor values can not be read for a non-node type '
                               'device!')
        self.device_data = node
        self.bmc_data = cfg.get_device(node.get("bmc"))
        self.plugin_name = node.get("oob_sensor", 'mock')
        return None
