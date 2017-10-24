# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""Unit tests"""
import unittest
import io
from threading import Thread
from mock import MagicMock, patch
import datastore
from ..dai_console_log import *


class TestDaiConsoleLog(unittest.TestCase):
    """Unit Tests for the DAI Console Log Class"""
    def setUp(self):
        DaiConsoleLog.SLEEP_TIME = 0.1
        datastore.get_logger = MagicMock()
        self.options = {}
        self.options['node_name'] = 'node'

    def tearDown(self):
        patch.stopall()

    def test_stop_capture(self):
        """Test start capture"""
        dai = DaiConsoleLog(**self.options)
        result = dai.start_log_capture('End', 'result')
        self.assertGreater(len(result), 0)

    @patch("control.console_log.dai_console_log.dai_console_log.Popen", Autospec=True)
    def test_stop_capture(self, mock_subprocess_popen):
        """Test start capture"""
        mock_subprocess_popen.return_value.return_code = 0
        mock_subprocess_popen.return_value.communicate.return_value = ('hello\nresult\nEnd' , "")
        dai = DaiConsoleLog(**self.options)
        result = dai.start_log_capture('End', 'result')
        self.assertGreater(len(result), 0)

    @patch("control.console_log.dai_console_log.dai_console_log.Popen", Autospec=True)
    def test_popen_exception(self, mock_subprocess_popen):
        mock_subprocess_popen.side_effect = Exception("error")
        dai = DaiConsoleLog(**self.options)
        with self.assertRaises(Exception):
            dai.start_log_capture('End', 'result')


if __name__ == '__main__':
    unittest.main()
