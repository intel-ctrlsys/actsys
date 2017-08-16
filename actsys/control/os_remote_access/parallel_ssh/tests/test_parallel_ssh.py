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
from pssh.pssh_client import ParallelSSHClient
from pssh import exceptions
from ..parallel_ssh import ParallelSshPlugin
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData


class MockRunOutput(object):
    def __init__(self, exit_code = 1, stdout=[], stderr=[], exception=None):
        self.stdout = stdout
        self.stderr = stderr
        self.exception = exception
        self.exit_code = exit_code

class TestRemoteSshPlugin(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""
    def setUp(self):
        manager = PluginManager()
        manager.register_plugin_class(ParallelSshPlugin)
        self.remote = manager.create_instance('os_remote_access', 'parallel_ssh')
        self.access = RemoteAccessData('127.0.0.1', 22, getpass.getuser(), None)

    @patch.object(ParallelSSHClient, "join")
    @patch.object(ParallelSSHClient, "run_command")
    def test_execute_run_stdout(self, mock_ssh, mock_join):
        """Test the RemoteSshPlugin.execute() method."""
        mock_ssh.return_value = {"localhost": MockRunOutput(stdout=["service test is enabled"])}
        result1 = self.remote.execute_multiple_nodes(['whoami'], [self.access])
        self.assertEqual(result1["localhost"].stderr, "service test is enabled\n")

    @patch.object(ParallelSSHClient, "join")
    @patch.object(ParallelSSHClient, "run_command")
    def test_execute_run_success(self, mock_ssh, mock_join):
        """Test the RemoteSshPlugin.execute() method."""
        mock_ssh.return_value = {"localhost": MockRunOutput(exit_code=0)}
        result1 = self.remote.execute_multiple_nodes(['service', 'status', 'firewalld'], [self.access])
        self.assertEqual(result1["localhost"].stdout, "Success: status - firewalld")

    @patch.object(ParallelSSHClient, "join")
    @patch.object(ParallelSSHClient, "run_command")
    def test_execute_run_stderr(self, mock_ssh, mock_join):
        """Test the RemoteSshPlugin.execute() method."""
        mock_ssh.return_value = {"localhost": MockRunOutput(stderr=["service test is not available"])}
        result1 = self.remote.execute_multiple_nodes(['whoami'], [self.access])
        self.assertEqual(result1["localhost"].stderr, "service test is not available\n")

    @patch.object(ParallelSSHClient, "join")
    @patch.object(ParallelSSHClient, "run_command")
    def test_execute_run_exception_1(self, mock_ssh, mock_join):
        """Test the RemoteSshPlugin.execute() method."""
        mock_ssh.return_value = {"localhost": MockRunOutput(exception="exception occurred")}
        result1 = self.remote.execute_multiple_nodes(['whoami'], [self.access])
        self.assertEqual(result1["localhost"].stderr, "exception occurred\n")

    @patch.object(ParallelSSHClient, "join")
    @patch.object(ParallelSSHClient, "run_command")
    def test_execute_run_exception_2(self, mock_ssh, mock_join):
        mock_ssh.return_value = None
        try:
            self.remote.execute_multiple_nodes(['whoami'], [self.access], capture=True)
            self.fail("No exception occurred!")
        except RuntimeError:
            pass

if __name__ == '__main__':
    unittest.main()
