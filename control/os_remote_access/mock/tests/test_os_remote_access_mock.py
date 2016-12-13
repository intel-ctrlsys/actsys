# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the mock remote OS access class.
"""
import unittest
from ..os_remote_access import PluginMetadata
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData


class TestMockPlugin(unittest.TestCase):
    """Test teh remote mocking class."""
    def test_metadata(self):
        """Test metadata class."""
        metadata = PluginMetadata()
        self.assertEqual('os_remote_access', metadata.category())
        self.assertEqual('mock', metadata.name())
        self.assertEqual(1000, metadata.priority())
        self.assertIsNotNone(metadata.create_instance())

    def test_api(self):
        """Test execute method"""
        manager = PluginManager()
        metadata = PluginMetadata()
        manager.add_provider(metadata)
        remote = manager.factory_create_instance(metadata.category(),
                                                 metadata.name())
        access = RemoteAccessData('127.0.0.1', 22, 'PASSWORD', None)
        remote.execute([], access, True, None)
        remote.execute([], access, False, None)

    def test_test_connection(self):
        manager = PluginManager()
        metadata = PluginMetadata()
        manager.add_provider(metadata)
        remote = manager.factory_create_instance(metadata.category(),
                                                 metadata.name())
        remote.dfx_result_list = [True, False, True]
        access = RemoteAccessData('127.0.0.1', 22, 'PASSWORD', None)
        self.assertTrue(remote.test_connection(access),
                        'First try expected True!')
        self.assertFalse(remote.test_connection(access),
                         'Second try expected False!')
        self.assertTrue(remote.test_connection(access),
                        'Third try expected True!')
        self.assertFalse(remote.test_connection(access),
                         'Fourth try expected a default of False!')
