# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the CrtlLogger class
"""

import re
import unittest
import logging
from mock import MagicMock
from ...commands import Command, CommandResult
from ..ctrl_logger import CtrlLogger, get_ctrl_logger
from ...plugin.manager import PluginManager

TEST_LOG = ".test.log"

class TestCtrlLogger(unittest.TestCase):
    """Tests for logging functionality"""

    def setUp(self):
        """Change log file location and create a logger"""
        CtrlLogger.LOG_FILE = TEST_LOG
        self.log = get_ctrl_logger()
        self.log.setLevel(logging.DEBUG)
        self.log.handlers[0].setLevel(logging.DEBUG)
        self.log_functions = {
            'DEBUG': self.log.debug,
            'INFO': self.log.info,
            'WARNING': self.log.warning,
            'ERROR' : self.log.error,
            'CRITICAL' : self.log.critical
        }

        self.reg = re.compile("\s+(\w+)\s+actsys:\s([^\n]+)")

    def msg_in_log_file(self, expected_msg):
        test_log = open(TEST_LOG, "r").read()
        logs = self.reg.findall(test_log)
        return expected_msg in logs

    def test_ctrl_logger_simple_message(self):
        """Test for a single message."""
        log_msg = "Dummy log message"
        for level, fnt  in self.log_functions.iteritems():
            fnt(log_msg)
            self.assertTrue(self.msg_in_log_file((level, log_msg)),
                            "{0} log message not found ".format(level))

    def test_ctrl_logger_with_args(self):
        """Test for log message with arguments"""
        msg = "Handling arguments %i %s"
        arg1= 1
        arg2 = "two"
        test_msg  = msg%(arg1,arg2)
        for level, fnt in self.log_functions.iteritems():
            fnt(msg, arg1, arg2)
            self.assertTrue(self.msg_in_log_file((level, test_msg)),
                            "{0} log message not found ".format(level))

    def test_ctrl_logger_with_kwargs(self):
        """Test for log message with kwargs"""
        dict_test = {'ip':'132.168.0.0', 'user':'testUser' }
        log_msg = 'Log with kwargs'
        for level, fnt in self.log_functions.iteritems():
            fnt(log_msg, dict_test)
            self.assertTrue(self.msg_in_log_file((level, log_msg)),
                            "{0} log message not found ".format(level))

    def test_ctrl_logger_multiple_msgs(self):
        """Tests with a list of messages"""
        messages = ["Dummy 1", "Dummy 2", "Dummy 3"]
        for level, fnt in self.log_functions.iteritems():
            fnt(messages)
            for single_msg in messages:
                self.assertTrue(self.msg_in_log_file((level, single_msg)),
                                "{0} log message not found ".format(level))

    def test_ctrl_logger_journal(self):
        """Test for journal logs """
        test_command = Command({'device_name': 'fake_node01',
                                'configuration': [],
                                'plugin_manager': PluginManager(),
                                'logger': None,
                                'arguments': ['5214']})

        test_command.get_name = MagicMock(return_value="PowerOnCommand")
        test_result = CommandResult(message='Switches are off', return_code=1)

        log_format = '%(cmd)s %(device)s, %(message)s'
        dict_fmt = {
            'cmd': 'power on',
            'device': test_command.device_name,
            'message': 'Job Started'
        }

        expected_msg = log_format % dict_fmt
        self.log.journal(test_command)
        self.assertTrue(self.msg_in_log_file(("JOURNAL", expected_msg)))

        dict_fmt['message'] = test_result.message
        expected_msg = log_format % dict_fmt
        self.log.journal(test_command, test_result)
        self.assertTrue(self.msg_in_log_file(("JOURNAL", expected_msg)))

    def test_ctrl_logger_singleton(self):
        """Test that get_ctrl_logger always returns the same instance"""
        my_log = get_ctrl_logger()
        my_other_log = get_ctrl_logger()
        self.assertEqual(my_log, my_other_log)

if __name__ == '__main__':
    unittest.main()
