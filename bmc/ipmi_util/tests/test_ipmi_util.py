"""
Test the IPMI plugin for BMC access/control.
"""
import os
import time
import unittest
from ctrl.bmc.ipmi_util.ipmi_util import PluginMetadata
from ctrl.plugin.manager import PluginManager
from ctrl.utilities.utilities import Utilities
from ctrl.os_remote_access.ssh.ssh import RemoteSshPlugin


class MockUtilities(Utilities):
    """Mock class fake low level system call helpers."""
    def __init__(self):
        Utilities.__init__(self)
        self.returned_value = None

    def execute_no_capture(self, command):
        """Execute a command list suppressing output and returning the return
           code."""
        if self.returned_value is None:
            return 0
        else:
            return self.returned_value

    def execute_with_capture(self, command):
        """Execute a command list capturing output and returning the return
           code, stdout, stderr"""
        return self.returned_value

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
        self.metadata = PluginMetadata()
        self.manager.add_provider(self.metadata)
        self.bmc = self.manager.factory_create_instance('bmc', 'ipmi_util')
        self.bmc.utilities = self.__utilities
        self.bmc.mandatory_bmc_wait_seconds = 0

    def wait_for_os(self, address, state):
        start_time = time.time()
        now = start_time
        self.bmc.utilities.returned_value = False
        while self.__utilities.ping_check(address) != state and \
                (now - start_time) < 300:
            time.sleep(1)
            now = time.time()
            self.bmc.utilities.returned_value = True

    def test_metadata_ipmi_util(self):
        self.assertEqual('bmc', self.metadata.category())
        self.assertEqual('ipmi_util', self.metadata.name())
        self.assertEqual(100, self.metadata.priority())
        self.assertIsNotNone(self.bmc)

    def test_get_chassis_state(self):
        self.bmc.utilities.returned_value = 'chassis_power = on'
        rv = self.bmc.get_chassis_state('127.0.0.1', 'admin', 'PASSWORD')
        self.assertTrue(rv)
        self.bmc.utilities.returned_value = 'chassis_power = off'
        rv = self.bmc.get_chassis_state('127.0.0.1', 'admin', 'PASSWORD')
        self.assertFalse(rv)
        self.bmc.utilities.returned_value = None
        with self.assertRaises(RuntimeError):
            self.bmc.get_chassis_state('127.0.0.1', 'admin', 'PASSWORD')
        self.bmc.utilities.returned_value = ''
        with self.assertRaises(RuntimeError):
            self.bmc.get_chassis_state('127.0.0.1', 'admin', 'PASSWORD')

    def test_set_chassis_state(self):
        self.bmc.utilities.returned_value = 0
        if self.__utilities.ping_check('127.0.0.2'):
            ssh = RemoteSshPlugin()
            ssh.utilities = self.__utilities
            ssh.utilities.returned_value = 0
            ssh.execute(['shutdown', '-H', 'now'], '127.0.0.2', 22, 'root')
            self.wait_for_os('127.0.0.2', False)
        with self.assertRaises(RuntimeError):
            self.bmc.set_chassis_state('127.0.0.1', 'admin', 'PASSWORD', 'red')
        self.bmc.set_chassis_state('127.0.0.1', 'admin', 'PASSWORD', 'bios')
        self.bmc.utilities.returned_value = 'chassis_power = on'
        rv = self.bmc.get_chassis_state('127.0.0.1', 'admin', 'PASSWORD')
        self.assertTrue(rv)
        self.bmc.utilities.returned_value = 0
        self.bmc.set_chassis_state('127.0.0.1', 'admin', 'PASSWORD', 'off')
        self.bmc.set_chassis_state('127.0.0.1', 'admin', 'PASSWORD', 'on')
        self.wait_for_os('127.0.0.2', True)

        self.bmc.tool = 'ls'
        with self.assertRaises(RuntimeError):
            self.bmc.set_chassis_state('127.0.0.1', 'admin', 'PASSWORD', 'off')

if __name__ == '__main__':
    unittest.main()
