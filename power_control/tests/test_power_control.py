# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests to test the interface for power_control.
"""
import unittest
from ctrl.power_control.power_control import PowerControl


class TestPowerControl(unittest.TestCase):
    """class to run the UT for the power_control interface."""
    def test_all_tests(self):
        """All tests."""
        interface = PowerControl()
        interface.get_current_device_power_state()
        interface.set_device_power_state('on', True)
