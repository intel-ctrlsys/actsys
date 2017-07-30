# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the job launch cli implementation.
"""
import unittest
import sys
from mock import MagicMock
from ..job_launch_cli import JobLaunchCli
from ..command_invoker import CommandInvoker


class TestProvisionCLI(unittest.TestCase):

    def setUp(self):
        self.mock_ci = MagicMock(spec=CommandInvoker)
        self.cli = JobLaunchCli(self.mock_ci)

    def test_help_msgs(self):
        commands = [
            ['launch', '-h'],
            ['check', '-h'],
            ['retrieve', '-o mock_file', '-h'],
            ['cancel', '-h'],
            ['-h']
        ]

        for command in commands:
            with self.assertRaises(SystemExit):
                self.cli.parse_and_run(command)

    def test_launch(self):
        self.cli.parse_and_run(['launch', 'mock_script'])
        self.mock_ci.job_launch.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <job_script>
            self.cli.parse_and_run(['launch'])

    def test_check(self):
        self.cli.parse_and_run(['check'])
        self.mock_ci.job_check.assert_called_once()

        with self.assertRaises(SystemExit):
            self.cli.parse_and_run(['check', '--args args'])

    def test_retrieve(self):
        self.cli.parse_and_run(['retrieve', 'job-1', '-o job-1.output'])
        self.mock_ci.job_retrieve.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <job_id>
            self.cli.parse_and_run(['retrieve'])

    def test_cancel(self):
        self.cli.parse_and_run(['cancel', 'job-1'])
        self.mock_ci.job_cancel.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <job_id>
            self.cli.parse_and_run(['cancel'])

    def test_argv(self):
        sys.argv = ['job', 'launch', 'mock_script']
        self.cli.parse_and_run()
        self.mock_ci.job_launch.assert_called_once()

        sys.argv = ['job', 'launch']
        with self.assertRaises(SystemExit):
            # missing arg <job_script>
            self.cli.parse_and_run()

    def test_exception(self):
        self.mock_ci.job_launch = MagicMock(side_effect=KeyError,
                                            return_value=3)

        result = self.cli.parse_and_run(['launch', 'mock_script'])
        self.assertEqual(result.return_code, 1)
