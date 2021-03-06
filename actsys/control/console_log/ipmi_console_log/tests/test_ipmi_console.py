# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""Unit tests"""
import unittest
import subprocess
import shutil, tempfile
from os import path
from mock import patch
from ..ipmi_console_log import *


class TestIpmiConsoleLog(unittest.TestCase):
    """Unit Tests for the IPMI Console Log Class"""
    def setUp(self):
        IpmiConsoleLog.SLEEP_TIME = 0.1
        self.test_dir = tempfile.mkdtemp()
        self.options = {}
        self.options['node_name'] = 'node'
        self.options['bmc_ip_address'] = 'bmc'
        self.options['bmc_user'] = 'user'
        self.options['bmc_password'] = None
        self.options['time_out'] = 1

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("control.console_log.ipmi_console_log.ipmi_console_log.Popen", Autospec=True)
    @patch("control.console_log.ipmi_console_log.ipmi_console_log.Thread")
    @patch.object(Timer, 'start')
    @patch.object(Timer, 'cancel')
    @patch.object(subprocess, 'Popen')
    def test_ipmi_thread_exception(self, mock_popen, mock_start, mock_cancel, thread_mock, mock_subprocess_popen):
        """Test start capture"""
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('Test.\nresult is here.\nEnd\n')
        mock_subprocess_popen.return_value = subprocess.Popen(['tail', '-f', path.join(self.test_dir, 'test.txt')],
                                                              stdout=PIPE, stderr=STDOUT, stdin=PIPE)
        mock_popen.return_value = subprocess.Popen('echo hello')
        mock_subprocess_popen.return_value.terminate.return_value = None

        ipmi = IpmiConsoleLog(**self.options)
        ipmi.start_log_capture('End', 'result')
        self.assertRaises(Exception)

    @patch("control.console_log.ipmi_console_log.ipmi_console_log.Popen", Autospec=True)
    @patch.object(Timer, 'start')
    @patch.object(Timer, 'cancel')
    @patch.object(subprocess, 'Popen')
    def test_ipmi_stop_capture(self, mock_popen,  mock_start, mock_cancel, mock_subprocess_popen):
        """Test start capture"""
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('Test.\nresult is here.\nEnd\n')
        mock_subprocess_popen.return_value = subprocess.Popen(['tail', '-f', path.join(self.test_dir, 'test.txt')],
                                                              stdout=PIPE, stderr=STDOUT, stdin=PIPE)
        mock_subprocess_popen.return_value.terminate.return_value = None
        mock_popen.return_value = subprocess.Popen('echo hello')
        mock_subprocess_popen.return_value.poll.return_code = None
        dai = IpmiConsoleLog(**self.options)
        result = dai.start_log_capture('End', 'result')
        self.assertGreater(len(result), 0)

    @unittest.skip
    @patch("control.console_log.ipmi_console_log.ipmi_console_log.Popen", Autospec=True)
    def test_ipmi_popen_exception(self, mock_subprocess_popen):
        mock_subprocess_popen.side_effect = Exception("error")
        dai = IpmiConsoleLog(**self.options)
        with self.assertRaises(Exception):
            dai.start_log_capture('End', 'result')


if __name__ == '__main__':
    unittest.main()
