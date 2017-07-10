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
        manager = PluginManager()
        manager.register_plugin_class(BmcMock)
        self.options = dict()
        self.options['plugin_manager'] = manager
        self.options['bmc_list'] = [{"access_type": "mock"}]

    def test_rest_power_constructor_with_no_options(self):
        try:
            RestPower()
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

    def test_rest_power_get_current_device_power_state_with_empty_bmc_list(self):
        self.options['bmc_list'] = []
        try:
            RestPower(**self.options).get_current_device_power_state()
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

    def test_rest_power_get_current_device_power_state_with_no_bmc_access_type(self):
        self.options['bmc_list'] = [{}]
        try:
            RestPower(**self.options).get_current_device_power_state()
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

    @patch.object(BmcMock, 'get_chassis_state')
    def test_rest_power_get_current_device_power_state(self, get_chassis_state):
        get_chassis_state.return_value = 'On'
        self.assertEqual(RestPower(**self.options).get_current_device_power_state(), 'On')

    @patch.object(BmcMock, 'set_chassis_state')
    def test_rest_power_set_device_power_state(self, set_chassis_state):
        set_chassis_state.return_value = True
        self.assertEqual(RestPower(**self.options).set_device_power_state('On'), True)
