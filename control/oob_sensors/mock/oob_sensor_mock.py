# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
OOB sensors mock class.
"""

from ...plugin import DeclarePlugin
from ..oob_sensors import OobSensor


@DeclarePlugin('mock', 1000)
class OobSensorMock(OobSensor):
    """Plugin for mocking Oob Sensor."""

    def __init__(self, device_name):
        OobSensor.__init__(self, device_name)
        self.device_name = device_name

    def get_sensor_value(self, sensor_name, device, bmc):
            sensor_name_f = self._get_sensor_name(sensor_name)
            return "{0} sensor value(s) is 10".format(sensor_name_f)

    def get_sensor_value_over_time(self, sensor_name, duration, sample_rate, device, bmc):
        sensor_name_f = self._get_sensor_name(sensor_name)
        sample = []
        for i in range(0, duration*sample_rate):
            sample.append(10)
        return "{0} sensor values over {1} at a sample rate of {2} are {3}".format(sensor_name_f, duration, sample_rate,
                                                                                   sample)

    @staticmethod
    def _get_sensor_name(sensor_name):
        if sensor_name == '.*':
            return 'All'
        else:
            return sensor_name
