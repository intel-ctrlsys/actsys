# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""Unit tests"""
import unittest
import subprocess
from mock import MagicMock, patch
import datastore
from ..ipmi_console_log import IpmiConsoleLog


class TestIpmiConsoleLog(unittest.TestCase):
    """Unit Tests for the IPMI Console Log Class"""
    def setUp(self):
        IpmiConsoleLog.SLEEP_TIME = 0.1
        datastore.get_logger = MagicMock()
        self.mock_subprocess_popen_patcher = patch.object(subprocess, "Popen")
        self.mock_subprocess_popen = self.mock_subprocess_popen_patcher.start()

    def tearDown(self):
        patch.stopall()
    #
    # @patch('datastore.get_logger')
    # @patch('subprocess.Popen')
    # @patch.object(Thread, 'start')
    # def test_start_capture(self, mock, subproc_mock, mock_thread):
    #     """Test start capture"""
    #     subproc_mock = MagicMock()
    #     mock_thread.start = MagicMock()
    #     ipmi = IpmiConsoleLog('node1', '127.0.0.1', 'admin', 'admin')
    #     ipmi.start_log_capture('End')
    #
    # @patch('datastore.get_logger')
    # @patch('subprocess.Popen')
    # @patch.object(Thread, 'start')
    # def test_start_capture_exception(self, mock, subproc_mock, mock_thread):
    #     """Test start capture"""
    #     ipmi = IpmiConsoleLog('node1', '127.0.0.1', 'admin', 'admin')
    # #     subproc_mock.side_effect = Exception
    #     ipmi.start_log_capture()

    def test_stop_capture(self):
        """Test start capture"""
        self.mock_subprocess_popen.return_value = subprocess.Popen('echo hello')
        self.mock_subprocess_popen.return_value.poll.return_code = True
        self.mock_subprocess_popen.return_value.stdout.readline.return_value = 'End'
        self.mock_subprocess_popen.return_value.wait.return_value = None
        self.mock_subprocess_popen.return_value.terminate.return_value = None
        ipmi = IpmiConsoleLog('a', 'b', 'c', 'None')
        result = ipmi.start_log_capture('End')
        self.assertGreater(len(result), 0)

    #
    # @patch('datastore.get_logger')
    # @patch.object(Utilities, 'execute_subprocess')
    # @patch.object(Thread, 'start')
    # def test_stop_capture_exception(self, mock, subproc_mock, mock_thread):
    #     """Test start capture"""
    #     ipmi = IpmiConsoleLog('node1', '127.0.0.1', 'admin', 'admin')
    #     subproc_mock.side_effect = Exception
    #     ipmi.stop_log_capture()

if __name__ == '__main__':
    unittest.main()
