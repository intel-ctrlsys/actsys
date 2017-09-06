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
        result = []
        num_sensors = self.sensor_name.split(',')
        for sensors in num_sensors:
            sensor_value = self.get_sensor_name(sensors)
            try:
                result_dict = self.oob_sensor_plugin.get_sensor_value(sensor_value, self.device_data, self.bmc_data)
                for key, value in result_dict.items():
                    p_ret_msg = self.print_table_border('Sensor Name', 'Values', key, sensor_value) + \
                                self.print_table_border('-', '-') + self.print_table(value)
                    command_result = CommandResult(0, p_ret_msg)
                    command_result.device_name = key
                    result.append(command_result)
            except RuntimeError as ex:
                result.append(CommandResult(255, str(ex)))
                continue
        return result
