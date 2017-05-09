# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
 Get oob sensor value
"""
from ...commands.command import CommandResult
from ...plugin import DeclarePlugin
from .oob_sensor_command import OobSensorCommand
from requests.exceptions import ConnectionError


@DeclarePlugin('oob_sensor_get', 100)
class OobSensorGetCommand(OobSensorCommand):
    """Oob Sensor get values"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, sensor_name=None):
        OobSensorCommand.__init__(self, device_name, configuration, plugin_manager, logger, sensor_name=sensor_name)
        self.sensor_name = sensor_name

    def execute(self):
        """Execute the command"""
        self.setup()
        self.oob_sensor_plugin = self.plugin_manager.create_instance('oob_sensors', self.plugin_name,
                                                                     device_name=self.device_name)

        try:
            ret_msg = self.oob_sensor_plugin.get_sensor_value(self.sensor_name, self.device_data, self.bmc_data)
        except RuntimeError as ex:
            return CommandResult(1, ex.message)
        p_ret_msg = self.print_table_border('Sensor Name', 'Values', self.device_name) + \
                    self.print_table_border('-', '-') + self.print_table(ret_msg)
        return CommandResult(0, p_ret_msg)

