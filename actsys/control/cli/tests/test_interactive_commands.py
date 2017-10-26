# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""Test file for Interactive CLI"""
from __future__ import print_function
from unittest import TestCase
import pytest
from mock import patch
from ..interactive_commands import CtrlCommands
from ...commands.command import CommandResult

class InteractiveCliTest(TestCase):
    """Tests for Interactive CLI"""
    @patch("control.cli.CommandInvoker")
    @patch('control.cli.interactive_commands.CtrlCommands.add_completer_options')
    def setUp(self, mock_command_invoker, mock_completer):
        self.control_cli_executor = CtrlCommands(0)
        self.node_name = 'test'
        self.mock_completer = mock_completer
        #Power/Bios/Job/Sensor
        mock_command_invoker.common_cmd_invoker.return_value = CommandResult(0, "Success")

        #Resource
        mock_command_invoker.resource_add.return_value = CommandResult(0, "Success")
        mock_command_invoker.resource_remove.return_value = CommandResult(0, "Success")
        mock_command_invoker.resource_check.return_value = CommandResult(0, "Success")

        #Service
        mock_command_invoker.service_status.return_value = CommandResult(0, "Success")
        mock_command_invoker.service_on.return_value = CommandResult(0, "Success")
        mock_command_invoker.service_off.return_value = CommandResult(0, "Success")

        #Provision
        mock_command_invoker.provision_add.return_value = CommandResult(0, "Success")
        mock_command_invoker.provision_delete.return_value = CommandResult(0, "Success")
        mock_command_invoker.provision_set.return_value = CommandResult(0, "Success")

        #Diag
        mock_command_invoker.diagnostics_inband.return_value = CommandResult(0, "Success")
        mock_command_invoker.diagnostics_oob.return_value = CommandResult(0, "Success")

        mock_command_invoker.bios_update.return_value = CommandResult(0, "Success")
        mock_command_invoker.bios_version.return_value = CommandResult(0, "Success")

        mock_command_invoker.oob_sensor_get.return_value = CommandResult(0, "Success")
        mock_command_invoker.oob_sensor_get_over_time.return_value = CommandResult(0, "Success")

        mock_command_invoker.job_launch.return_value = CommandResult(0, "Success")
        mock_command_invoker.job_check.return_value = CommandResult(0, "Success")
        mock_command_invoker.job_cancel.return_value = CommandResult(0, "Success")
        self.control_cli_executor.ctrl_command_invoker = mock_command_invoker

    def test_power_cmd_execute(self):
        """Testing Power Commands"""
        for action in ['on', 'off', 'cycle', 'bios', 'efi', 'hdd', 'pxe', 'cdrom', 'removable']:
            cmd = action + ' -d' + self.node_name
            self.control_cli_executor.power(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_resource_cmd_execute(self):
        """Testing Resource Commands"""
        for action in ['add', 'remove', 'check']:
            cmd = action + ' -d ' + self.node_name
            self.control_cli_executor.resource(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_service_cmd_execute(self):
        """Testing Service Commands"""
        for action in ['status', 'start', 'stop']:
            cmd = action + ' -d' + self.node_name
            self.control_cli_executor.service(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_provision_cmd_execute(self):
        """Testing Provision Commands"""
        for action in ['add', 'delete', 'set']:
            cmd = action + ' -d' + self.node_name
            self.control_cli_executor.provision(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_diag_cmd_execute(self):
        """Testing Diagnotic Commands"""
        for action in ['inband', 'oob']:
            cmd = action + ' -d' + self.node_name
            self.control_cli_executor.diag(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_bios_cmd_execute(self):
        """Testing Bios Commands"""
        for action in ['update', 'get-version']:
            cmd = action + ' -d' + self.node_name
            self.control_cli_executor.bios(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_sensor_cmd_execute(self):
        """Testing Sensor Commands"""
        sensor_name = 'sensor'
        for action in ['get', 'get_over_time']:
            cmd = action + ' ' + sensor_name + ' -d' + self.node_name
            self.control_cli_executor.sensor(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_job_cmd_execute(self):
        """Testing Job Commands"""
        job_name = 'job'
        for action in ['launch', 'check', 'cancel']:
            cmd = action + ' -j' + job_name
            self.control_cli_executor.job(cmd)
            out, err = self.capsys.readouterr()
            assert "Success" in out
            assert err == ""

    def test_get_cmd_execute(self):
        for option in ['freq', 'powercap']:
            self.control_cli_executor.get(option)
            out, err = self.capsys.readouterr()
            assert "Command not implemented" in out
            assert err == ""

    def test_set_cmd_execute(self):
        for option in ['freq', 'powercap']:
            self.control_cli_executor.set(option)
            out, err = self.capsys.readouterr()
            assert "Command not implemented" in out
            assert err == ""

    def test_process_cmd_execute(self):
        for option in ['list', 'kill']:
            self.control_cli_executor.process(option)
            out, err = self.capsys.readouterr()
            assert "Command not implemented" in out
            assert err == ""

    def test_menu(self):
        self.control_cli_executor.menu(None)

    @pytest.fixture(autouse=True)
    def set_capsys(self, capsys):
        """Capsys"""
        self.capsys = capsys
