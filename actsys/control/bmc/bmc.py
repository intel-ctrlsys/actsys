# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This defines the interface for BMC objects.
"""
from ..plugin import DeclareFramework


@DeclareFramework('bmc')
class Bmc(object):
    """Interface class for bmc classes."""
    def __init__(self):
        pass

    def get_chassis_state(self, remote_access_object):
        """Get the current chassis state for a node."""
        pass

    def set_chassis_state(self, remote_access_object, new_state):
        """Set the target chassis state for a node."""
        pass

    def get_version(self, device_list, bmc_list):
        """Read the bios image info for a compute node"""
        pass

    def bios_update(self, device_list, bmc_list, image):
        """Update bios on a compute node"""
        pass

    def get_sensor_value(self, sensor_name, device_list, bmc_list):
        """Read the sensor values for a compute node"""
        pass

    def get_sensor_value_over_time(self, sensor_name, duration, sample_rate, device_list, bmc_list):
        """Read the sensor values of a compute node  over specified
        time duration at specified sample rate"""
        pass
