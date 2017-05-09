# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
 Get oob sensor value over time
"""
import math
from ...commands.command import CommandResult
from ...plugin import DeclarePlugin
from .oob_sensor_command import OobSensorCommand


@DeclarePlugin('oob_sensor_get_time', 100)
class OobSensorGetTimeCommand(OobSensorCommand):
    """Oob Sensor get values over time"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, sensor_name=None, duration=None,
                 sample_rate=None):
        OobSensorCommand.__init__(self, device_name, configuration, plugin_manager, logger, sensor_name=sensor_name,
                                  duration=duration, sample_rate=sample_rate)
        self.sensor_name = sensor_name
        self.sample_rate = sample_rate
        self.duration = duration

    def execute(self):
        """Execute the command"""
        self.setup()
        sensor_name = self.sensor_name
        sample_rate = self._convert_str_to_num(self.sample_rate)
        duration = self._convert_str_to_num(self.duration)

        if duration == 0 or sample_rate == 0:
            raise RuntimeError("Duration and Sample_rate must be greater than 1")
        self.oob_sensor_plugin = self.plugin_manager.create_instance('oob_sensors', self.plugin_name,
                                                                     device_name=self.device_name)
        try:
            ret_msg = self.oob_sensor_plugin.get_sensor_value_over_time(sensor_name, duration, sample_rate,
                                                                        self.device_data, self.bmc_data)
        except RuntimeError as ex:
            return CommandResult(1, ex.message)
        p_ret_msg = self.print_table_border('Sensor Name', 'Values', self.device_name) + self.print_table_border('-', '-') \
                    + self.print_table(ret_msg)
        return CommandResult(0, p_ret_msg)

    @staticmethod
    def _convert_str_to_num(num):

        try:
            value = int(num)
            return value
        except ValueError:
            try:
                value = float(num)
                return int(math.floor(value))
            except ValueError:
                raise RuntimeError("Duration and Sample_rate cannot take strings as arguments")
