# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the node_power plugin implementation.
"""
import unittest
from ctrl.power_control.nodes.node_power import PluginMetadata as NodePowerMD
from ctrl.bmc.mock.bmc import PluginMetadata as BmcMD
from ctrl.os_remote_access.mock.os_remote_access import PluginMetadata as OsMD
from ctrl.utilities.utilities import Utilities
from ctrl.plugin.manager import PluginManager
from ctrl.utilities.remote_access_data import RemoteAccessData
from ctrl.bmc.mock.bmc import BmcMock
from ctrl.power_control.nodes.node_power import NodePower


class MockUtilities(Utilities):
    """Mock class fake low level system call helpers."""
    def __init__(self):
        Utilities.__init__(self)
        self.stack = []
        self.ping_stack = []

    def execute_no_capture(self, command):
        """Execute a command list suppressing output and returning the return
           code."""
        if len(self.stack) == 0:
            return 0
        else:
            result = self.stack[0]
            self.stack = self.stack[1:]
            return result

    def execute_with_capture(self, command):
        """Execute a command list capturing output and returning the return
           code, stdout, stderr"""
        if len(self.stack) == 0:
            return ''
        else:
            result = self.stack[0]
            self.stack = self.stack[1:]
            return result

    def ping_check(self, address):
        """Check if a network address has a OS responding to pings."""
        if len(self.ping_stack) == 0:
            return True
        else:
            value = self.ping_stack[0]
            self.ping_stack = self.ping_stack[1:]
            return value


class MockSwitch(object):
    """Mock class for switches (PDUs)"""
    def __init__(self):
        self.state = True

    def get_switch_state(self, access, outlet):
        """Return the mocked state."""
        return self.state


class MockOsAccess(object):
    """Mock up OS access plugin for certain tests."""
    def __init__(self, options=None):
        self.stack = []

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Mocked call to execute."""
        if len(self.stack) == 0:
            return 0, None
        else:
            result = self.stack[0]
            self.stack = self.stack[1:]
            if result:
                return 0, None
            else:
                return 255, None


class MockBmcAccess(BmcMock):
    """Mock the bmc mock class."""
    def __init__(self, options=None):
        BmcMock.__init__(self, options)
        self.state_stack = []
        self.set_failure = False

    def get_chassis_state(self, remote_access):
        """Get the fake chassis state."""
        if len(self.state_stack) == 0:
            return True
        else:
            result = self.state_stack[0]
            self.state_stack = self.state_stack[1:]
            return result


class MockNodePower(NodePower):
    """Mocking parts of NodePower."""
    def __init__(self, options):
        NodePower.__init__(self, options)
        self.shutdown_succeed = None
        self.graceful_fail = False

    def wait_for_chassis_state(self, state, timeout):
        """Test access to _wait_for_chassis_state()"""
        return self._wait_for_chassis_state(state, timeout)

    def graceful_os_halt(self):
        """Mock the graceful shutdown to fail."""
        return self.shutdown_succeed

    def _graceful_os_halt(self):
        if self.graceful_fail:
            self.graceful_fail = False
            return False
        else:
            return NodePower._graceful_os_halt(self)


class TestNodePower(unittest.TestCase):
    """Test the NodePower class."""
    def setUp(self):
        self.__utilities = MockUtilities()
        self.manager = PluginManager()
        self.metadata = NodePowerMD()
        self.manager.add_provider(NodePowerMD())
        self.manager.add_provider(BmcMD())
        self.manager.add_provider(OsMD())
        self.os_access = RemoteAccessData('127.0.0.1', 22, 'admin', None)
        self.bmc_access = RemoteAccessData('127.0.0.2', 0, 'admin', None)
        self.bmc_plugin = self.manager.factory_create_instance('bmc', 'mock')
        self.bmc_plugin.set_chassis_state(self.bmc_access, 'off')
        self.os_plugin = MockOsAccess()
        self.switch_access1 = RemoteAccessData('127.0.0.3', 22, 'admin', None)
        self.switch_access2 = RemoteAccessData('127.0.0.3', 22, 'admin', None)
        self.switch_plugin1 = MockSwitch()
        self.switch_plugin2 = MockSwitch()
        self.__options = {
            'device_name': 'test_node',
            'device_type': 'node',
            'os': (self.os_access, self.os_plugin),
            'bmc': (self.bmc_access, self.bmc_plugin),
            'switches': [
                (self.switch_access1, self.switch_plugin1, '3'),
                (self.switch_access2, self.switch_plugin2, '1')
            ],
            'policy': {
                'OSShutdownTimeoutSeconds': 2,
                'OSBootTimeoutSeconds': 2,
                'OSNetworkToHaltTime': 2,
                'BMCBootTimeoutSeconds': 2,
                'BMCChassisOffWait': 2
            }
        }

        self.controller = self.manager.factory_create_instance('power_control',
                                                               'node_power',
                                                               self.__options)
        self.controller.utilities = self.__utilities

    def test_ctor(self):
        self.assertIsNotNone(self.controller)

    def test_metadata(self):
        self.assertEqual('power_control', self.metadata.category())
        self.assertEqual('node_power', self.metadata.name())
        self.assertEqual(100, self.metadata.priority())

    def test_no_options(self):
        with self.assertRaises(RuntimeError):
            self.controller = self.manager.factory_create_instance(
                    'power_control',
                    'node_power')

    def test_get_current_device_power_state(self):
        self.__utilities.returned_value = True
        result = self.controller.get_current_device_power_state()
        self.assertEqual('Off', result)

    def test_set_device_power_state(self):
        result = self.controller.set_device_power_state('On:bios')
        self.assertTrue(result)
        self.__utilities.ping_stack = [True,  False]
        result = self.controller.set_device_power_state('Off')
        self.assertTrue(result)
        self.__utilities.ping_stack = [False, True]
        result = self.controller.set_device_power_state('On:bmc_on')
        self.assertTrue(result)
        self.__utilities.ping_stack = [False, True]
        result = self.controller.set_device_power_state('On')
        self.assertTrue(result)

    def test__parse_options(self):
        self.__options['device_type'] = 'network_switch'
        with self.assertRaises(RuntimeError):
            self.manager.factory_create_instance('power_control', 'node_power',
                                                 self.__options)
        self.__options['device_type'] = 'node'
        self.__options['os'] = (None, self.os_plugin)
        with self.assertRaises(RuntimeError):
            self.manager.factory_create_instance('power_control', 'node_power',
                                                 self.__options)
        self.__options['os'] = (self.os_access, None)
        with self.assertRaises(RuntimeError):
            self.manager.factory_create_instance('power_control', 'node_power',
                                                 self.__options)
        self.__options['os'] = (self.os_access, self.os_plugin)
        self.__options['bmc'] = (None, self.bmc_plugin)
        with self.assertRaises(RuntimeError):
            self.manager.factory_create_instance('power_control', 'node_power',
                                                 self.__options)
        self.__options['bmc'] = (self.bmc_access, None)
        with self.assertRaises(RuntimeError):
            self.manager.factory_create_instance('power_control', 'node_power',
                                                 self.__options)
        self.__options['bmc'] = (self.bmc_access, self.bmc_plugin)
        self.__options['switches'] = None
        self.__options['policy'] = None
        self.manager.factory_create_instance('power_control',
                                             'node_power', self.__options)
        self.__options['policy'] = {}
        self.manager.factory_create_instance('power_control',
                                             'node_power', self.__options)

    def test_switches_exceptions(self):
        self.switch_plugin2.state = False
        with self.assertRaises(RuntimeError):
            self.controller.get_current_device_power_state()

    def test_set_with_off(self):
        result = self.controller.set_device_power_state('Off')
        self.assertTrue(result)
        result = self.controller.set_device_power_state('On:bmc_on')
        self.assertTrue(result)
        self.os_plugin.stack = [(255, None)]
        result = self.controller.set_device_power_state('Off')
        self.assertFalse(result)
        self.__utilities.ping_stack = [False, True]
        result = self.controller.set_device_power_state('On:bmc_on')
        self.assertTrue(result)
        self.bmc_plugin.set_failure = True
        self.__utilities.ping_stack = [True, False]
        result = self.controller.set_device_power_state('Off')
        self.assertFalse(result)
        self.bmc_plugin.set_failure = False

    def test_wait_for_chassis_state(self):
        mock_bmc = MockBmcAccess()
        self.__options['bmc'] = (self.bmc_access, mock_bmc)
        power = MockNodePower(self.__options)
        mock_bmc.state_stack = [False, True]
        result = power.wait_for_chassis_state(True, 3)
        self.assertTrue(result)

    def test_target_on_to_state(self):
        mock_os = MockOsAccess()
        self.__options['os'] = (self.os_access, mock_os)
        power = NodePower(self.__options)
        power.utilities = self.__utilities
        self.assertTrue(power.set_device_power_state('On:on'))
        self.__utilities.ping_stack = [True, False]
        self.assertTrue(power.set_device_power_state('On:efi'))

    def test_target_on_to_state_2(self):
        mock_os = MockOsAccess()
        self.__options['os'] = (self.os_access, mock_os)
        power = MockNodePower(self.__options)
        power.utilities = self.__utilities
        self.__utilities.ping_stack = [False, True]
        self.assertTrue(power.set_device_power_state('On'))
        self.__utilities.ping_stack = [True, False]
        self.assertTrue(power.set_device_power_state('On:efi'))

    def test_target_off(self):
        mock_os = MockOsAccess()
        self.__options['os'] = (self.os_access, mock_os)
        power = MockNodePower(self.__options)
        power.utilities = self.__utilities
        self.assertTrue(power.set_device_power_state('On:efi'))
        self.__utilities.ping_stack = [False]
        result = power.get_current_device_power_state()
        self.assertEqual('On', result)
        self.__utilities.ping_stack = [False]
        self.assertTrue(power.set_device_power_state('Off'))

    def test_target_off_force(self):
        mock_os = MockOsAccess()
        self.__options['os'] = (self.os_access, mock_os)
        power = MockNodePower(self.__options)
        power.utilities = self.__utilities
        self.assertTrue(power.set_device_power_state('On:bmc_on'))
        self.__utilities.ping_stack = [True]
        result = power.get_current_device_power_state()
        self.assertEqual('On:bmc_on', result)
        self.__utilities.ping_stack = [True]
        self.assertTrue(power.set_device_power_state('Off', True))

    def test_target_on_force(self):
        mock_os = MockOsAccess()
        self.__options['os'] = (self.os_access, mock_os)
        power = MockNodePower(self.__options)
        power.utilities = self.__utilities
        self.assertTrue(power.set_device_power_state('On:bmc_on'))
        self.__utilities.ping_stack = [True]
        result = power.get_current_device_power_state()
        self.assertEqual('On:bmc_on', result)
        mock_os.stack = [False, False]
        self.graceful_fail = True
        self.__utilities.ping_stack = [True, False]
        self.assertTrue(power.set_device_power_state('On:bmc_on', True))

    def test__do_bmc_power_state(self):
        mock_os = MockOsAccess()
        mock_bmc = MockBmcAccess()
        self.__options['os'] = (self.os_access, mock_os)
        self.__options['bmc'] = (self.bmc_access, mock_bmc)
        power = MockNodePower(self.__options)
        power.utilities = self.__utilities
        mock_bmc.state_stack = [False, False]
        mock_bmc.set_failure = True
        self.assertFalse(power.set_device_power_state('On:bmc_on'))

    def test_target_on_shutdown_failed(self):
        mock_os = MockOsAccess()
        self.__options['os'] = (self.os_access, mock_os)
        power = MockNodePower(self.__options)
        power.utilities = self.__utilities
        self.assertTrue(power.set_device_power_state('On:bmc_on'))
        self.__utilities.ping_stack = [True]
        result = power.get_current_device_power_state()
        self.assertEqual('On:bmc_on', result)
        self.graceful_fail = True
        self.__utilities.ping_stack = [True]
        self.assertFalse(power.set_device_power_state('On:bmc_on'))
