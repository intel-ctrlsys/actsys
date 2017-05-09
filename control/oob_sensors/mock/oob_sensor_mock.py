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
        result = dict()
        sample = list()
        sample.append(10)
        sensor_name_f = self._get_sensor_name(sensor_name)
        result[sensor_name_f] = sample
        return result

    def get_sensor_value_over_time(self, sensor_name, duration, sample_rate, device, bmc):
        sensor_name_f = self._get_sensor_name(sensor_name)
        result = dict()
        sample = []
        for i in range(0, duration*sample_rate):
            sample.append(10)
        result[sensor_name_f] = sample
        return result

    @staticmethod
    def _get_sensor_name(sensor_name):
        if sensor_name == '.*':
            return 'All sensors'
        else:
            return sensor_name
