# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the rest_power plugin implementation.
"""
import unittest
from ..rest_power import RestPower
from mock import patch
from ....bmc.mock.bmc import BmcMock
from ....plugin.manager import PluginManager


class TestRestPower(unittest.TestCase):
    """Test the RestPower class."""
    def setUp(self):
        self.manager = PluginManager()
        self.manager.register_plugin_class(BmcMock)
        self.bmc_plugin = self.manager.create_instance('bmc', 'mock')

    def test_rest_power_constructor_with_no_options(self):
        try:
            RestPower()
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

    def test_rest_power_get_current_device_power_state_with_bad_device_type(self):
        options = {
            'device_type': 'bad_type',
            'bmc': ("bmc_access", self.bmc_plugin)
        }
        try:
            RestPower(**options).get_current_device_power_state()
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

    def test_rest_power_get_current_device_power_state_with_no_bmc_credebtials(self):
        options = {
            'device_type': 'node',
            'bmc': (None, self.bmc_plugin)
        }
        try:
            RestPower(**options).get_current_device_power_state()
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

    def test_rest_power_get_current_device_power_state_with_no_bmc_plugin(self):
        options = {
            'device_type': 'node',
            'bmc': ("bmc_access", None)
        }
        try:
            RestPower(**options).get_current_device_power_state()
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

    @patch.object(BmcMock, 'get_chassis_state')
    def test_rest_power_get_current_device_power_state(self, get_chassis_state):
        get_chassis_state.return_value = 'On'
        options = {
            'device_type': 'node',
            'bmc': ("bmc_access", self.bmc_plugin)
        }
        self.assertEqual(RestPower(**options).get_current_device_power_state(), 'On')

    @patch.object(BmcMock, 'set_chassis_state')
    def test_rest_power_set_device_power_state(self, set_chassis_state):
        set_chassis_state.return_value = True
        options = {
            'device_type': 'node',
            'bmc': ("bmc_access", self.bmc_plugin)
        }
        self.assertEqual(RestPower(**options).set_device_power_state('On'), True)


