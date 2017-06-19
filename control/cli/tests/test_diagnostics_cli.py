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
            ['inband', '-h'],
            ['oob', '-h'],
            ['-h']
        ]

        for command in commands:
            with self.assertRaises(SystemExit):
                self.cli.parse_and_run(command)

    def test_inband(self):
        self.cli.parse_and_run(['inband', 'test-1', '--image', 'image_test'])
        self.mock_ci.diagnostics_inband.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run(['inband'])

    def test_oob(self):
        self.cli.parse_and_run(['oob', 'test-1'])
        self.mock_ci.diagnostics_oob.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run(['oob'])

    def test_argv(self):
        sys.argv = ['diag', 'inband', 'test-1', '--image', 'image_test']
        self.cli.parse_and_run()
        self.mock_ci.diagnostics_inband.assert_called_once()

        sys.argv = ['diag', 'inband']
        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run()

    def test_exception(self):
        self.mock_ci.diagnostics_inband = MagicMock(side_effect=KeyError, return_value=3)

        result = self.cli.parse_and_run(['inband', 'test-1', '--image', 'image_test'])
        self.assertEqual(result.return_code, 1)
