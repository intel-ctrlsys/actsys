# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the mock_resource_control plugin implementation.
"""
import unittest
import sys
from mock import patch, MagicMock
from ..provision_cli import ProvisionCli
from ..command_invoker import CommandInvoker

class TestProvisionCLI(unittest.TestCase):

    def setUp(self):
        self.mock_ci = MagicMock(spec=CommandInvoker)
        self.cli = ProvisionCli(self.mock_ci)

    def test_help_msgs(self):
        commands = [
            ['add', '-h'],
            ['delete', '-h'],
            ['set', '-h'],
            ['set', '--ipaddr=127.0.0.1', '-h'],
            ['-h']
        ]

        for command in commands:
            with self.assertRaises(SystemExit):
                self.cli.parse_and_run(command)

    def test_add(self):
        self.cli.parse_and_run(['add', 'test-1'])
        self.mock_ci.provision_add.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run(['add'])

    def test_delete(self):
        self.cli.parse_and_run(['delete', 'test-1'])
        self.mock_ci.provision_delete.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run(['delete'])

    def test_set(self):
        self.cli.parse_and_run(['set', 'test-1'])
        self.mock_ci.provision_set.assert_called_once()

        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run(['set'])

    def test_argv(self):
        sys.argv = ['provision', 'add', 'test-1']
        self.cli.parse_and_run()
        self.mock_ci.provision_add.assert_called_once()

        sys.argv = ['provision', 'add']
        with self.assertRaises(SystemExit):
            # missing arg <device_name>
            self.cli.parse_and_run()

    def test_exception(self):
        self.mock_ci.provision_add = MagicMock(side_effect=KeyError, return_value=3)

        result = self.cli.parse_and_run(['add', 'test-1'])
        self.assertEqual(result.return_code, 1)
