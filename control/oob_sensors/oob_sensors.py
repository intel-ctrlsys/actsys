# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Interface for oob sensors reading framework.
"""
from ..plugin import DeclareFramework


@DeclareFramework('oob_sensors')
class OobSensor(object):
    def __init__(self, device_name):
        pass

    def get_sensor_value(self, sensor_name, device_data, node_data):
        """Read the sensor values for a compute node"""
        pass

    def get_sensor_value_over_time(self, sensor_name, duration, sample_rate, device_data, node_data):
        """Read the sensor values of a compute node  over specified
        time duration at specified sample rate"""
        pass
