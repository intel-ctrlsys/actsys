# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Common fixtures for the power commands.
"""
import unittest
import os
import json
from ctrl.plugin.manager import PluginManager
from ctrl.power_control.mock.power_control_mock import PluginMetadata as \
    NodePowerMetadata
from ctrl.power_control.mock.power_control_mock import PowerControlMock
from ctrl.bmc.mock.bmc import PluginMetadata as BmcMetadata
from ctrl.os_remote_access.mock.os_remote_access import PluginMetadata as \
    RemoteMetadata
from ctrl.utilities.remote_access_data import RemoteAccessData


class MockConfiguration(object):
    """Mock the configuration object"""

    def __init__(self):
        self.data = dict()

    def get_device_data(self, device_name, param):
        """Dummy getter"""
        key = '{}.{}'.format(device_name, param)
        return self.data[key]

    def set_device_data(self, device_name, param, value):
        """Dummy setter"""
        key = '{}.{}'.format(device_name, param)
        self.data[key] = value


class MockPowerPlugin(PowerControlMock):
    """Pre-programmed responses"""
    def __init__(self, options=None):
        super(MockPowerPlugin, self).__init__(options)

    def set_device_power_state(self, target_state, force_on_failure=False):
        return False


class MockPowerPluginException(PowerControlMock):
    """Pre-programmed responses"""
    def __init__(self, options=None):
        super(MockPowerPluginException, self).__init__(options)

    def set_device_power_state(self, target_state, force_on_failure=False):
        raise RuntimeError('Mock exception')


class PowerCommandsCommon(unittest.TestCase):
    """Common to all power common tests"""
    def setUp(self):
        self.node_name = 'test_node'
        self.persistent_file = os.path.join(os.path.sep, 'tmp',
                                            self.node_name + '.state')
        self.manager = PluginManager()
        self.manager.add_provider(NodePowerMetadata())
        self.manager.add_provider(BmcMetadata())
        self.manager.add_provider(RemoteMetadata())
        self.configuration = MockConfiguration()
        self.setUpConfiguration()
        self.command_options = {
            'device_name': 'test_node',
            'configuration': self.configuration,
            'plugin_manager': self.manager,
            'logger': None,
            'arguments': ['off']
        }
        self.options = {
            'device_name': self.node_name,
            'device_type': 'node',
            'os': (object(), object()),
            'bmc': (object(), object()),
            'switches': [],
            'policy': {
                'OSShutdownTimeoutSeconds': 150,
                'OSBootTimeoutSeconds': 300,
                'OSNetworkToHaltTime': 5,
                'BMCBootTimeoutSeconds': 10,
                'BMCChassisOffWait': 3
            }
        }

    def tearDown(self):
        file_name = os.path.join(os.path.sep, 'tmp', 'test_node.state')
        if os.path.exists(file_name):
            os.unlink(file_name)

    def _setter(self, param, value):
        setter = self.configuration.set_device_data
        setter('test_node', param, value)

    def setUpConfiguration(self):
        """Setup a configuration object for mocking"""
        setter = self.configuration.set_device_data

        # OS
        os_info = RemoteAccessData('192.168.128.50', 22, 'admin', None)
        self._setter('access_type', 'mock')
        self._setter('remote_access', os_info)
        self._setter('device_type', 'compute')
        self._setter('device_power_control', 'mock')
        self._setter('bmc_device_name', 'bmc_test_node')
        self._setter('switches', [])

        # BMC
        bmc_info = RemoteAccessData('192.168.128.51', 623, 'admin', 'PASSWORD')
        setter('bmc_test_node', 'remote_access', bmc_info)
        setter('bmc_test_node', 'device_type', 'bmc')
        setter('bmc_test_node', 'access_type', 'mock')

    def write_state(self, state):
        """Write out a node power state to the mocked storage location"""
        descriptor = open(self.persistent_file, 'w')
        json.dump(state, descriptor)
        descriptor.close()
