# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the RemoteSshPlugin.
"""
import getpass
import unittest
from mock import patch
from ..ssh import RemoteSshPlugin
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData
from ....utilities.utilities import Utilities, SubprocessOutput


class TestRemoteSshPlugin(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""
    def setUp(self):
        manager = PluginManager()
        manager.register_plugin_class(RemoteSshPlugin)
        self.remote = manager.create_instance('os_remote_access', 'ssh')
        self.access = RemoteAccessData('127.0.0.1', 22, getpass.getuser(), None)

    @patch.object(Utilities, "execute_no_capture")
    def test_test_connection(self, mock_enc):
        mock_enc.return_value = 0
        rv = self.remote.test_connection(self.access)
        self.assertTrue(rv, 'Could not verify ssh with 127.0.0.1!')

        mock_enc.return_value = 1
        rv = self.remote.test_connection(self.access)
        self.assertFalse(rv, 'Could not verify ssh with 127.0.0.1!')

        mock_enc.return_value = 123
        rv = self.remote.test_connection(self.access)
        self.assertFalse(rv, 'Could not verify ssh with 127.0.0.1!')

    @patch.object(Utilities, "execute_subprocess")
    @patch.object(Utilities, "execute_no_capture")
    def test_execute_1(self, mock_nc, mock_esub):
        """Test the RemoteSshPlugin.execute() method."""
        mock_nc.return_value = 0
        result1 = self.remote.execute(['whoami'], self.access)
        mock_esub.return_value = SubprocessOutput(0, 'John Doe', "He's the best!")
        result2 = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual(0, result1.return_code)
        self.assertIsNone(result1.stdout)
        self.assertEqual(0, result2.return_code)
        self.assertEqual('John Doe', result2.stdout)

    @patch.object(Utilities, "execute_no_capture")
    def test_execute_2(self, mock_utilities):
        """Test of execute part 2."""
        mock_utilities.return_value = 0
        self.access.identifier = 'id'
        result = self.remote.execute(['whoami'], self.access)
        self.assertEqual(0, result.return_code)

    @patch.object(Utilities, "execute_subprocess")
    def test_execute_3(self, mock_esub):
        self.access.port = 22222
        mock_esub.return_value = SubprocessOutput(0, 'John Doe', "He's the best!")
        result = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual(0, result.return_code)
        self.assertEqual('John Doe', result.stdout)

    @patch.object(Utilities, "execute_subprocess")
    def test_execute_4(self, mock_esub):
        self.access.port = 22222
        mock_esub.return_value = SubprocessOutput(123, None, None)
        result = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual(123, result.return_code)


if __name__ == '__main__':
    unittest.main()
