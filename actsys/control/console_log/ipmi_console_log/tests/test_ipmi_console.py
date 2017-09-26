# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""Unit tests"""
import unittest
import subprocess
import io
from threading import Thread
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

    def test_stop_capture(self):
        """Test start capture"""
        self.mock_subprocess_popen.return_value = subprocess.Popen('echo hello')
        self.mock_subprocess_popen.return_value.poll.return_code = None
        self.mock_subprocess_popen.return_value.stdout.readline.return_value = 'hello\nresult\nEnd'
        self.mock_subprocess_popen.return_value.wait.return_value = None
        self.mock_subprocess_popen.return_value.terminate.return_value = None
        ipmi = IpmiConsoleLog('a', 'b', 'c', 'None')
        result = ipmi.start_log_capture('End', 'result')
        self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()
