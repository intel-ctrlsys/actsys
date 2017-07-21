# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for Interface to satisfy code coverage.
"""
import unittest
from ..bmc import Bmc
from ...utilities.remote_access_data import RemoteAccessData


class TestInterface(unittest.TestCase):
    """Tests for the BMC Interface class"""
    def setUp(self):
        """Common setup for tests."""
        self.interface = Bmc()
        self.remote = RemoteAccessData('127.0.0.2', 0, 'admin', 'PASSWORD')

    def test_interface(self):
        self.interface.get_chassis_state(self.remote)
        self.interface.set_chassis_state(self.remote, 'on')
        self.interface.get_version(None, None)
        self.interface.bios_update(None, None, 'test.bin')

    def test_oob_sensor(self):
        self.interface.get_sensor_value_over_time('none', 'none', 'none', None, None)
        self.interface.get_sensor_value('name', None, None)
