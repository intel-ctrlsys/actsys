# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright (c) 2016 Intel Corp.
#
"""
This module creates the command line parser and executes the user commands.
"""

import argparse
from cli_cmd_invoker import CommandExeFactory


class CtrlCliParser(object):
    """Control Parser Class"""

    CLI_COMMAND = "ctrl"

    def __init__(self):
        """Init Function for Control Cli Parser"""

        self.ctrl_parser = argparse.ArgumentParser(prog='ctrl',
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

    def add_subparser(self, parser_name, parser_help, subcommand_choices=list(),
                      subcommand_help=None, arg_list_kwargs=list()):
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

        # Additional arguments that are applied to all commands (at the end).
        subparser.add_argument('device_name', help='Device where command will be executed.')

        return subparser

    def add_simple_args(self):
        """Add the simple arguments here"""
        self.ctrl_parser.add_argument("-V", "--version", action="version", version='0.1.0',
                                      help='Provides the version of the tool')

    def get_all_args(self):
        return self.ctrl_parser.parse_args()


class CtrlCliExecutor(object):
    """This class executes the commands based on user's request"""

    def __init__(self):
        try:
            self.cmd_exe_factory_obj = CommandExeFactory()
        except Exception as f:
            if hasattr(f, 'value'):
                print (f.value)
            else:
                print (f)
            from sys import exit
            exit(1)

    def power_cmd_execute(self, cmd_args):
        """Function to call appropriate power sub-command"""
        if cmd_args.subcommand == 'off':
            return self.cmd_exe_factory_obj.power_off_invoker(cmd_args.device_name, cmd_args.subcommand,
                                                              cmd_args)
        elif cmd_args.subcommand == 'cycle':
            return self.cmd_exe_factory_obj.power_cycle_invoker(cmd_args.device_name, cmd_args.subcommand,
                                                                cmd_args)
        else:
            return self.cmd_exe_factory_obj.power_on_invoker(cmd_args.device_name, cmd_args.subcommand,
                                                             cmd_args)

    def process_cmd_execute(self, cmd_args):
        """Function to call appropriate process sub-command"""
        if cmd_args.subcommand == 'list':
            print("\tProcess List Command called\n"
                  "\tHowever for this command work is in progress.\n"
                  "\tSo hold your breath till we develop this module\n")
            return 0
        else:
            print("\tProcess Kill Command Called\n"
                  "\tHowever for this command work is in progress.\n"
                  "\tSo hold your breath till we develop this module\n")
            return 0

    def resource_cmd_execute(self, cmd_args):
        """Function to call appropriate resource sub-command"""
        if cmd_args.subcommand == 'add':
            return self.cmd_exe_factory_obj.resource_add(cmd_args.device_name, cmd_args)
        elif cmd_args.subcommand == 'remove':
            return self.cmd_exe_factory_obj.resource_remove(cmd_args.device_name, cmd_args)
        elif cmd_args.subcommand == 'check':
            return self.cmd_exe_factory_obj.resource_check(cmd_args.device_name, cmd_args)
        else:
            print ("Invalid resource command entered.")
        return 1

    def get_cmd_execute(self, cmd_args):
        """Function to call appropriate get sub-command"""
        if cmd_args.subcommand == 'powercap':
            print("\tGet Powercap Command Called\n"
                  "\tHowever for this command work is in progress.\n"
                  "\tSo hold your breath till we develop this module\n")
            return 0
        else:
            print("\tGet Freq Command Called\n"
                  "\tHowever for this command work is in progress.\n"
                  "\tSo hold your breath till we develop this module\n")
            return 0

    def set_cmd_execute(self, cmd_args):
        """Function to call appropriate set sub-command"""
        if cmd_args.subcommand == 'powercap':
            print("\tSet Powercap Command Called\n"
                  "\tHowever for this command work is in progress.\n"
                  "\tSo hold your breath till we develop this module\n")
            return 0
        else:
            print("\tSet Freq Command Called\n"
                  "\tHowever for this command work is in progress.\n"
                  "\tSo hold your breath till we develop this module\n")
            return 0

    def service_cmd_execute(self, cmd_args):
        """Function to call appropriate resource sub-command"""
        if cmd_args.subcommand == 'status':
            return self.cmd_exe_factory_obj.service_status(cmd_args.device_name, cmd_args)
        elif cmd_args.subcommand == 'start':
            return self.cmd_exe_factory_obj.service_on(cmd_args.device_name, cmd_args)
        elif cmd_args.subcommand == 'stop':
            return self.cmd_exe_factory_obj.service_off(cmd_args.device_name, cmd_args)
        else:
            print ("Invalid service command entered.")
        return 1

    def execute_cli_cmd(self):
        """Function to call appropriate sub-parser"""
        masterparser = CtrlCliParser()
        cmd_args = masterparser.get_all_args()
        if cmd_args.subparser_name == 'power':
            retval = self.power_cmd_execute(cmd_args)
            return retval
        elif cmd_args.subparser_name == 'process':
            retval = self.process_cmd_execute(cmd_args)
            return retval
        elif cmd_args.subparser_name == 'resource':
            retval = self.resource_cmd_execute(cmd_args)
            return retval
        elif cmd_args.subparser_name == 'get':
            retval = self.get_cmd_execute(cmd_args)
            return retval
        elif cmd_args.subparser_name == 'set':
            retval = self.set_cmd_execute(cmd_args)
            return retval
        elif cmd_args.subparser_name == 'service':
            retval = self.service_cmd_execute(cmd_args)
            return retval
        else:
            return 0
