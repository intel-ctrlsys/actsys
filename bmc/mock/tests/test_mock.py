"""
Test the Mock plugin for BMC access/control.
"""
import os
import unittest
from ctrl.bmc.mock.mock import PluginMetadata
from ctrl.bmc.mock.mock import BmcMock
from ctrl.plugin.manager import PluginManager


class TestBmcMock(unittest.TestCase):
    def setUp(self):
        self.bmc_file = os.path.sep + os.path.join('tmp', 'bmc_file')

    def test_metadata_mock(self):
        manager = PluginManager()
        metadata = PluginMetadata()
        self.assertEqual('bmc', metadata.category())
        self.assertEqual('mock', metadata.name())
        self.assertEqual(1000, metadata.priority())
        manager.add_provider(metadata)
        bmc = manager.factory_create_instance('bmc', 'mock')
        self.assertIsNotNone(bmc)

    def test_persist_state(self):
        if os.path.exists(self.bmc_file):
            os.unlink(self.bmc_file)
        bmc = BmcMock()
        self.assertEqual(5, bmc.state_change_delay)
        address = '127.0.0.1'
        self.assertEqual('off', bmc.get_chassis_state(address, '', ''))
        bmc.set_chassis_state(address, '', '', 'on')
        with self.assertRaises(RuntimeError):
            bmc.set_chassis_state(address, '', '', 'crazy')
        self.assertEqual('on', bmc.get_chassis_state(address, '', ''))

        bmc = BmcMock()
        self.assertEqual('on', bmc.get_chassis_state(address, '', ''))
