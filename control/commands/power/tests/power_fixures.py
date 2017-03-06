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
from mock import patch, MagicMock
from datastore import DataStoreLogger
from ....plugin.manager import PluginManager
from ....power_control.mock.power_control_mock import PowerControlMock as NodePowerMetadata
from ....power_control.mock.power_control_mock import PowerControlMock
from ....bmc.mock.bmc import BmcMock as BmcMetadata
from ....pdu.mock.mock import PduMock as PduMetadata
from ....os_remote_access.mock.os_remote_access import OsRemoteAccessMock as RemoteMetadata
from ....resource.tests.mock_resource_control import MockResourceControl as RCPluginMetaData
from ....utilities.remote_access_data import RemoteAccessData
from ...resource_pool.resource_pool_add import ResourcePoolAddCommand as PRAdd
from ...resource_pool.resource_pool_check import ResourcePoolCheckCommand as RCpluginMeta
from ...resource_pool.resource_pool_remove import ResourcePoolRemoveCommand as PRRemove
from ...services import ServicesStatusCommand, ServicesStartCommand, ServicesStopCommand


class MockConfiguration(object):
    """Mock the configuration object"""

    class Object(object):
        """pass"""
        pass

    def __init__(self):
        self.data = dict()

    def get_node(self, device_name):
        """Dummy getter"""
        return self.data[device_name]

    def get_pdu(self, device_name):
        """Dummy getter"""
        return self.data[device_name]

    def get_device(self, device_name):
        """Dummy getter"""
        return self.data[device_name]

    def get_device_data(self, device_name, param):
        """Dummy getter"""
        if not self.data.has_key(device_name):
            return None
        return getattr(self.data[device_name], param)

    def set_device_data(self, device_name, param, value):
        """Dummy setter"""
        if self.data.get(device_name, None) is None:
            self.data[device_name] = {}
        self.data[device_name][param] = value


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

    class Object(object):
        """pass"""
        pass

    def setUp(self):
        self.node_name = 'test_node'
        self.persistent_file = os.path.join(os.path.sep, 'tmp', self.node_name + '.state')
        self.manager = PluginManager()
        self.manager.register_plugin_class(NodePowerMetadata)
        self.manager.register_plugin_class(BmcMetadata)
        self.manager.register_plugin_class(PduMetadata)
        self.manager.register_plugin_class(RemoteMetadata)
        self.manager.register_plugin_class(RCPluginMetaData)
        self.manager.register_plugin_class(PRAdd)
        self.manager.register_plugin_class(RCpluginMeta)
        self.manager.register_plugin_class(PRRemove)
        self.manager.register_plugin_class(ServicesStopCommand)
        self.manager.register_plugin_class(ServicesStartCommand)
        self.manager.register_plugin_class(ServicesStatusCommand)
        self.configuration = MockConfiguration()
        self.setUpConfiguration()
        self.args = self.Object()
        setattr(self.args, "subcommand", "off")
        setattr(self.args, "force", False)
        self.command_options = {
            'device_name': self.node_name,
            'configuration': self.configuration,
            'plugin_manager': self.manager,
            'logger': MagicMock(spec=DataStoreLogger),
            'arguments': self.args
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
        self._setter('device_type', 'node')
        self._setter('device_power_control', 'mock')
        self._setter('bmc_device_name', 'bmc_test_node')
        self._setter('switches', [])

        # BMC
        bmc_info = RemoteAccessData('192.168.128.51', 623, 'admin', 'PASSWORD')
        setter('bmc_test_node', 'remote_access', bmc_info)
        setter('bmc_test_node', 'device_type', 'bmc')
        setter('bmc_test_node', 'access_type', 'mock')

        setter(self.node_name, 'device_id', self.node_name)
        setter(self.node_name, 'access_type', 'mock')
        setter(self.node_name, 'service_list', ['slurm'])
        setter(self.node_name, 'resource_controller', 'mock')
        setter(self.node_name, 'ip_address', '192.168.128.50')
        setter(self.node_name, 'port', 22)
        setter(self.node_name, 'user', 'admin')
        setter(self.node_name, 'password', None)
        setter(self.node_name, 'os_shutdown_timeout_seconds', 150)
        setter(self.node_name, 'os_boot_timeout_seconds', 300)
        setter(self.node_name, 'os_network_to_halt_time', 5)
        setter(self.node_name, 'bmc_boot_timeout_seconds', 10)
        setter(self.node_name, 'bmc_chassis_off_wait', 3)

        # PDU
        setter('test_pdu', 'device_name', 'test_pdu')
        setter('test_pdu', 'device_type', 'pdu')
        setter('test_pdu', 'access_type', 'mock')
        setter('test_pdu', 'ip_address', '192.168.1.1')
        setter('test_pdu', 'port', 22)
        setter('test_pdu', 'password', 'pass')
        setter('test_pdu', 'user', 'admin')

    def write_state(self, state):
        """Write out a node power state to the mocked storage location"""
        descriptor = open(self.persistent_file, 'w')
        json.dump(state, descriptor)
        descriptor.close()
