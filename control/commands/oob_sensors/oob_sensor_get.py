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


@DeclarePlugin('oob_sensor_get', 100)
class OobSensorGetCommand(OobSensorCommand):
    """Oob Sensor get values"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, sensor_name=None):
        OobSensorCommand.__init__(self, device_name, configuration, plugin_manager, logger, sensor_name=sensor_name)
        self.sensor_name = sensor_name

    def execute(self):
        """Execute the command"""
        self.setup()
        final_return = ''
        self.oob_sensor_plugin = self.plugin_manager.create_instance('bmc', self.plugin_name)
        num_sensors = self.sensor_name.split(',')
        for sensors in num_sensors:
            sensor_value = self.get_sensor_name(sensors)
            try:
                ret_msg = self.oob_sensor_plugin.get_sensor_value(sensor_value, self.device_data, self.bmc_data)
            except RuntimeError as ex:
                final_return += ex.message
                continue
            p_ret_msg = self.print_table_border('Sensor Name', 'Values', self.device_name, sensor_value) + \
                        self.print_table_border('-', '-') + self.print_table(ret_msg)
            final_return += p_ret_msg
        return CommandResult(0, final_return)
