# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the RemoteSshPlugin.
"""
import getpass
import unittest
from ..ssh import RemoteSshPlugin
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData
from ....utilities.utilities import Utilities


class MockUtilities(Utilities):
    """Mock class fake low level system call helpers."""
    def __init__(self):
        super(MockUtilities, self).__init__()
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


class TestRemoteSshPlugin(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""
    def setUp(self):
        manager = PluginManager()
        manager.register_plugin_class(RemoteSshPlugin)
        self.remote = manager.create_instance('os_remote_access', 'ssh')
        self.remote.utilities = MockUtilities()  # Mocking
        self.access = RemoteAccessData('127.0.0.1', 22, getpass.getuser(), None)

    def test_test_connection(self):
        rv = self.remote.test_connection(self.access)
        self.assertTrue(rv, 'Could not verify ssh with 127.0.0.1!')

    def test_execute_1(self):
        """Test the RemoteSshPlugin.execute() method."""
        rv1, output = self.remote.execute(['whoami'], self.access)
        self.remote.utilities.returned_value = '', ''
        rv2, output = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual(0, rv1)
        self.assertEqual(0, rv2)

    def test_execute_2(self):
        """Test of execute part 2."""
        self.remote.utilities.returned_value = 0
        self.access.identifier = 'id'
        result = self.remote.execute(['whoami'], self.access)[0]
        self.assertEqual(0, result)

    def test_execute_3(self):
        self.access.port = 22222
        self.remote.utilities.returned_value = '', ''
        result = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual((0, ''), result)

    def test_execute_4(self):
        self.access.port = 22222
        self.remote.utilities.returned_value = None, None
        result = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual((255, None), result)


if __name__ == '__main__':
    unittest.main()
