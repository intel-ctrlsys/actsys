# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the IPMI plugin for BMC access/control.
"""
import time
import unittest
from mock import patch
from ..ipmi_util import BmcIpmiUtil
from ....plugin.manager import PluginManager
from ....utilities.utilities import Utilities, SubprocessOutput
from ....utilities.remote_access_data import RemoteAccessData


class MockUtilities(Utilities):
    """Mock class fake low level system call helpers."""
    def __init__(self):
        Utilities.__init__(self)
        self.returned_value = None

    def ping_check(self, address):
        """Check if a network address has a OS responding to pings."""
        if self.returned_value is None:
            return True
        else:
            return self.returned_value


class TestBmcIpmi(unittest.TestCase):
    """Test the ipmi_util bmc implementation."""
    def setUp(self):
        self.__utilities = MockUtilities()
        self.manager = PluginManager()
        self.manager.register_plugin_class(BmcIpmiUtil)
        self.bmc = self.manager.create_instance('bmc', 'ipmi_util')
        # self.bmc.utilities = self.__utilities
        self.bmc.mandatory_bmc_wait_seconds = 0
        self.bmc_credentials = RemoteAccessData('127.0.0.2', 0, 'admin',
                                                'PASSWORD')

    def wait_for_os(self, address, state):
        start_time = time.time()
        now = start_time
        self.bmc.utilities.returned_value = False
        while self.__utilities.ping_check(address) != state and \
                (now - start_time) < 300:
            time.sleep(0.01)
            now = time.time()
            self.bmc.utilities.returned_value = True

    @patch.object(Utilities, "execute_subprocess")
    def test_get_chassis_state(self, mock_esub):
        mock_esub.return_value = SubprocessOutput(0, 'chassis_power = on', '')
        rv = self.bmc.get_chassis_state(self.bmc_credentials)
        self.assertTrue(rv)
        mock_esub.return_value = SubprocessOutput(0, 'chassis_power = off', '')
        rv = self.bmc.get_chassis_state(self.bmc_credentials)
        self.assertFalse(rv)
        mock_esub.return_value = SubprocessOutput(1, None, None)
        with self.assertRaises(RuntimeError):
            self.bmc.get_chassis_state(self.bmc_credentials)
        mock_esub.return_value = SubprocessOutput(0, None, None)
        with self.assertRaises(RuntimeError):
            self.bmc.get_chassis_state(self.bmc_credentials)
        self.bmc.utilities.returned_value = SubprocessOutput(1, '', '')
        with self.assertRaises(RuntimeError):
            self.bmc.get_chassis_state(self.bmc_credentials)

    @patch.object(Utilities, "execute_subprocess")
    @patch.object(Utilities, "execute_no_capture")
    def test_set_chassis_state(self, mock_enc, mock_esub):
        mock_enc.return_value = 0
        with self.assertRaises(RuntimeError):
            self.bmc.set_chassis_state(self.bmc_credentials, 'red')
        self.bmc.set_chassis_state(self.bmc_credentials, 'bios')
        mock_esub.return_value = SubprocessOutput(0, 'chassis_power = on', '')
        rv = self.bmc.get_chassis_state(self.bmc_credentials)
        self.assertTrue(rv)
        mock_enc.return_value = 0
        self.bmc.set_chassis_state(self.bmc_credentials, 'off')
        self.bmc.set_chassis_state(self.bmc_credentials, 'on')
        self.wait_for_os(self.bmc_credentials.address, True)

        self.bmc.tool = 'ls'
        mock_enc.return_value = 1
        with self.assertRaises(RuntimeError):
            self.bmc.set_chassis_state(self.bmc_credentials, 'off')

if __name__ == '__main__':
    unittest.main()
