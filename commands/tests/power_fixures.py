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
        self.persistent_file = os.path.sep + \
            os.path.join('tmp', self.node_name + '.state')
        self.manager = PluginManager()
        self.manager.add_provider(NodePowerMetadata())
        self.command_options = {
            'device_name': 'test_node',
            'configuration': object(),
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
        file_name = os.path.sep + os.path.join('tmp', 'test_node.state')
        if os.path.exists(file_name):
            os.unlink(file_name)

    def write_state(self, state):
        """Write out a node power state to the mocked storage location"""
        descriptor = open(self.persistent_file, 'w')
        json.dump(state, descriptor)
        descriptor.close()
