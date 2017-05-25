# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

import unittest
import sys
from mock import patch, MagicMock
from ..diagnostics_cli import DiagnosticsCli
from ..command_invoker import CommandInvoker

class TestDiagnosticsCLI(unittest.TestCase):

    def setUp(self):
        self.mock_ci = MagicMock(spec=CommandInvoker)
        self.cli = DiagnosticsCli(self.mock_ci)

    def test_help_msgs(self):
        commands = [
            ['online', '-h'],
            ['offline', '-h'],
            ['-h']
        ]

        for command in commands:
            with self.assertRaises(SystemExit):
                self.cli.parse_and_run(command)

    def test_online(self):
        self.cli.parse_and_run(['online', 'test-1'])
        self.mock_ci.diagnostics_online.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run(['online'])

    def test_offline(self):
        self.cli.parse_and_run(['offline', 'test-1'])
        self.mock_ci.diagnostics_offline.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run(['offline'])

    def test_argv(self):
        sys.argv = ['diag', 'online', 'test-1']
        self.cli.parse_and_run()
        self.mock_ci.diagnostics_online.assert_called_once()

        sys.argv = ['diag', 'online']
        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run()

    def test_exception(self):
        self.mock_ci.diagnostics_online = MagicMock(side_effect=KeyError, return_value=3)

        result = self.cli.parse_and_run(['online', 'test-1'])
        self.assertEqual(result.return_code, 1)
