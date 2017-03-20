# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the RemoteTelnetPlugin.
"""
import unittest
from ....utilities.remote_access_data import RemoteAccessData
from ..telnet import RemoteTelnetPlugin
from mock import patch


class TestRemoteTelnetPlugin(unittest.TestCase):
    """Test case for the RemoteTelnetPlugin class."""

    def setUp(self):
        self.access1 = RemoteAccessData('', 0, '', '')
        self.access2 = RemoteAccessData('', 0, 'user', 'pass')
        self.old_sleep_time = RemoteTelnetPlugin.SLEEP_TIME
        self.old_timeout = RemoteTelnetPlugin.TIMEOUT
        RemoteTelnetPlugin.SLEEP_TIME = 0.2
        RemoteTelnetPlugin.TIMEOUT = 0.1

    def tearDown(self):
        RemoteTelnetPlugin.SLEEP_TIME = self.old_sleep_time
        RemoteTelnetPlugin.TIMEOUT = self.old_timeout

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
