# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the Mock plugin for BMC access/control.
"""
import os
import unittest
from ..bmc import BmcMock
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData


class TestBmcMock(unittest.TestCase):
    def setUp(self):
        self.bmc_file = os.path.join(os.path.sep, 'tmp', 'bmc_file')
        self.remote = RemoteAccessData('127.0.0.2', 0, 'admin', 'root')

    def test_metadata_mock(self):
        manager = PluginManager()
        manager.register_plugin_class(BmcMock)
        bmc = manager.create_instance('bmc', 'mock')
        self.assertIsNotNone(bmc)

    def test_persist_state(self):
        if os.path.exists(self.bmc_file):
            os.unlink(self.bmc_file)
        bmc = BmcMock()
        self.assertEqual(5, bmc.state_change_delay)
        self.assertFalse(bmc.get_chassis_state(self.remote))
        bmc.set_chassis_state(self.remote, 'on')
        with self.assertRaises(RuntimeError):
            bmc.set_chassis_state(self.remote, 'crazy')
        self.assertTrue(bmc.get_chassis_state(self.remote))

        bmc = BmcMock()
        self.assertTrue(bmc.get_chassis_state(self.remote))
