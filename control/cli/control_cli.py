# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright (c) 2016 Intel Corp.
#
"""
This module creates the command line parser and executes the user commands.
"""

from __future__ import print_function

import argparse
import sys
from datastore.datastore_cli import DataStoreCLI
from .command_invoker import CommandInvoker
from ..commands import CommandResult
from .provision_cli import ProvisionCli


class ControlArgParser(object):
    """Control Parser Class"""

    CLI_COMMAND = "ctrl"

    def __init__(self):
        """Init Function for Control Cli Parser"""

        self.ctrl_parser = argparse.ArgumentParser(prog=self.CLI_COMMAND,
                                                   description='Control Component Parser')

        self.ctrl_subparser = self.ctrl_parser.add_subparsers(
            title='Sub Commands',
            description='List of Valid Sub Commands', dest='subparser_name')

        self.add_simple_args()

        """Sub Parser for all Cli Commands"""
        self.add_subparser('power', 'Power on/off/reset a device.',
                           ['on', 'off', 'cycle', 'bios', 'efi', 'hdd', 'pxe', 'cdrom', 'removable'],
                           'Select an option: on/off/cycle/bios/efi/hdd/pxe/cdrom/removable.'
                           ' Ex: {} power on node001'.format(self.CLI_COMMAND),
                           [
                               {
                                   'name': '-f',
                                   'name2': '--force',
                                   'action': 'store_true',
                                   'help': 'This option will allow user to force the Power On/Off/Reboot'
                               },
                               {
                                   'name': '-o',
                                   'name2': '--outlet',
                                   'type': int,
                                   'nargs': '?',
                                   'help': 'Specify the outlet to edit (PDUs only)'
                               }
                           ])

        self.add_subparser('resource', 'Resource add/remove from a resource pool.', ['add', 'remove', 'check'],
                           'Select one of the following options: add/remove/check'
                           ' Ex: {} resource add node001'.format(self.CLI_COMMAND))

        self.add_subparser('process', 'Process list/kill on a node in a cluster.', ['list', 'kill'],
                           'Select one of two options: list/kill.'
                           ' Ex: {} process kill 1232 node001'.format(self.CLI_COMMAND),
                           [
                               {
                                   'name': 'process_id',
                                   'help': 'Please provide process id to list or kill a process'
                               }
                           ])

        self.add_subparser('get', 'Get powercap/freq value of a node.', ['freq', 'powercap'])

        self.add_subparser('set', 'Set powercap/freq value of a node.', ['freq', 'powercap'], 'Select an option to set',
                           [
                               {
                                   'name': 'value',
                                   'help': 'Please provide the value to be set'
                               }
                           ])

        self.add_subparser('service', 'Check, start or stop services specified in the configuration file',
                           ['status', 'start', 'stop'], 'Select an action to perform')

        self.ctrl_subparser.add_parser('datastore', help='Access and edit items found in the DataStore')
        self.ctrl_subparser.add_parser('provision', help='Provision nodes and set information about those nodes')

        self.add_subparser('bios', 'Update or get version of bios on specified nodes/group of nodes',
                           ['update', 'get-version'], 'Select an action to perform',
                           [
                               {
                                   'name': '-i',
                                   'name2': '--image',
                                   'nargs': '?',
                                   'help': 'Specify the bios image'
                               }
                           ])

    def add_subparser(self, parser_name, parser_help, subcommand_choices=list(),
                      subcommand_help=None, arg_list_kwargs=list(), require_device_name=True):
        """
        Helper function to add sub-parsers to ctrl. Note that device_name is added to the commands as the last arg.
        """
        subparser = self.ctrl_subparser.add_parser(parser_name, help=parser_help)
        subparser.add_argument('subcommand', choices=subcommand_choices, help=subcommand_help)

        # additional arguments the user wants
        for arg_kwarg in arg_list_kwargs:
            # To the developer: arg_kwarg.pop will throw a key error is name is not specified in the arg_kwarg dict
            #    this is intentional, please supply it.
            name2 = arg_kwarg.pop('name2', None)
            if name2 is not None:
                # Optional args
                subparser.add_argument(arg_kwarg.pop('name'), name2, **arg_kwarg)
            else:
                # positional args
                subparser.add_argument(arg_kwarg.pop('name'), **arg_kwarg)

        if require_device_name:
            # Additional arguments that are applied to all commands (at the end).
            subparser.add_argument('device_name', help='Device where command will be executed.')

        return subparser

    def add_simple_args(self):
        """Add the simple arguments here"""
        self.ctrl_parser.add_argument("-V", "--version", action="version", version='0.1.0',
                                      help='Provides the version of the tool')

    def get_all_args(self, args=None):
        if args is not None:
            return self.ctrl_parser.parse_args(args)
        else:
            return self.ctrl_parser.parse_args()


class ControlCommandLineInterface(object):
    """This class executes the commands based on user's request"""

    def __init__(self):
        try:
            self.cmd_invoker = CommandInvoker()
        except Exception as f:
            if hasattr(f, 'value'):
                print(f.value)
            else:
                print(f)
            sys.exit(1)

    def power_cmd_execute(self, cmd_args):
        """Function to call appropriate power sub-command"""
        if cmd_args.subcommand == 'off':
            return self.cmd_invoker.power_off_invoker(cmd_args.device_name, cmd_args.subcommand,
                                                      cmd_args.force, cmd_args.outlet)
        elif cmd_args.subcommand == 'cycle':
            return self.cmd_invoker.power_cycle_invoker(cmd_args.device_name, cmd_args.subcommand,
                                                        cmd_args.force, cmd_args.outlet)
        else:
            return self.cmd_invoker.power_on_invoker(cmd_args.device_name, cmd_args.subcommand,
                                                     cmd_args.force, cmd_args.outlet)

    def process_cmd_execute(self, cmd_args):
        """Function to call appropriate process sub-command"""
        if cmd_args.subcommand == 'list':
            return CommandResult(0, "Command not implemented: Process List Command called")
        else:
            return CommandResult(0, "Command not implemented: Process Kill Command Called")

    def resource_cmd_execute(self, cmd_args):
        """Function to call appropriate resource sub-command"""
        if cmd_args.subcommand == 'add':
            return self.cmd_invoker.resource_add(cmd_args.device_name)
        elif cmd_args.subcommand == 'remove':
            return self.cmd_invoker.resource_remove(cmd_args.device_name)
        elif cmd_args.subcommand == 'check':
            return self.cmd_invoker.resource_check(cmd_args.device_name)
        else:
            return CommandResult(1, "Invalid resource command entered.")

    def get_cmd_execute(self, cmd_args):
        """Function to call appropriate get sub-command"""
        if cmd_args.subcommand == 'powercap':
            return CommandResult(0, "Command not implemented: Get Powercap Command Called")
        else:
            return CommandResult(0, "Command not implemented: Get Freq Command Called")

    def set_cmd_execute(self, cmd_args):
        """Function to call appropriate set sub-command"""
        if cmd_args.subcommand == 'powercap':
            return CommandResult(0, "Command not implemented: Set Powercap Command Called")
        else:
            return CommandResult(0, "Command not implemented: Set Freq Command Called")

    def service_cmd_execute(self, cmd_args):
        """Function to call appropriate resource sub-command"""
        if cmd_args.subcommand == 'status':
            return self.cmd_invoker.service_status(cmd_args.device_name)
        elif cmd_args.subcommand == 'start':
            return self.cmd_invoker.service_on(cmd_args.device_name)
        elif cmd_args.subcommand == 'stop':
            return self.cmd_invoker.service_off(cmd_args.device_name)
        else:
            return CommandResult(1, "Invalid service command entered")

    def bios_cmd_execute(self, cmd_args):
        if cmd_args.subcommand == 'update':
            return self.cmd_invoker.bios_update(cmd_args.device_name, cmd_args.image)
        elif cmd_args.subcommand == 'get-version':
            return self.cmd_invoker.bios_version(cmd_args.device_name)
        else:
            return CommandResult(1, "Invalid bios command entered")

    def execute_cli_cmd(self):
        """Function to call appropriate sub-parser"""
        masterparser = ControlArgParser()

        # Following this pattern: http://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
        if len(sys.argv) >= 2 and sys.argv[1] == 'datastore':
            datastore_cli = DataStoreCLI(self.cmd_invoker.get_datastore()).parse_and_run(sys.argv[2:])
            return datastore_cli
        if len(sys.argv) >= 2 and sys.argv[1] == 'provision':
            provisioner_result = ProvisionCli(self.cmd_invoker).parse_and_run(sys.argv[2:])
            return self.handle_command_result(provisioner_result)

        cmd_args = masterparser.get_all_args()
        command_result = None
        if cmd_args.subparser_name == 'power':
            command_result = self.power_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'process':
            command_result = self.process_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'resource':
            command_result = self.resource_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'get':
            command_result = self.get_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'set':
            command_result = self.set_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'service':
            command_result = self.service_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'bios':
            command_result = self.bios_cmd_execute(cmd_args)

        return self.handle_command_result(command_result)

    def handle_command_result(self, command_result):
        """

        :param command_result:
        :return:
        """
        if isinstance(command_result, list):
            num_failures = 0
            for cr in command_result:
                if cr.return_code != 0:
                    print(cr, file=sys.stderr)
                    num_failures += 1
                else:
                    print(cr)
            num_commands = len(command_result)
            print("Result: {}/{} devices were successful".format(num_commands - num_failures, num_commands))
            return num_failures
        else:
            if command_result.return_code != 0:
                print(command_result, file=sys.stderr)
            else:
                print(command_result)
            return command_result.return_code
