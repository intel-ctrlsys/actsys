# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the RemoteTelnetPlugin.
"""
import unittest
from ..telnet import PluginMetadata
from ....utilities.remote_access_data import RemoteAccessData
from ..telnet import RemoteTelnetPlugin
from mock import patch


class TestRemoteTelnetPlugin(unittest.TestCase):
    """Test case for the RemoteTelnetPlugin class."""

    def setUp(self):
        self.access1 = RemoteAccessData('', 0, '', '')
        self.access2 = RemoteAccessData('', 0, 'user', 'pass')

    def test_plugin_metadata(self):
        """Test metadata."""
        meta = PluginMetadata()
        self.assertEqual('os_remote_access', meta.category())
        self.assertEqual('telnet', meta.name())
        self.assertEqual(100, meta.priority())
        self.assertIsNotNone(meta.create_instance())

    def test_test_connection(self):
        with self.assertRaises(NotImplementedError):
            telnet_session = RemoteTelnetPlugin()
            telnet_session.test_connection(self.access2)

    @patch('telnetlib.Telnet')
    def test_execute1(self, mock_telnet):
        telnet_session = RemoteTelnetPlugin()
        op1 = telnet_session.execute('ls', self.access1)
        self.assertIsNotNone(op1)
        op2 = telnet_session.execute('ls', self.access2)
        self.assertIsNotNone(op2)

    def test_execute2(self):
        """Test the RemoteTelnetPlugin.execute() method."""
        telnet_session = RemoteTelnetPlugin()
        op = telnet_session.execute('ls', self.access1)
        self.assertRaises(EnvironmentError)
        self.assertIsNone(op)
