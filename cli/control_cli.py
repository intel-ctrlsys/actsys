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

    def __init__(self):
        """Init Function for Control Cli Parser"""

        self.ctrl_parser = argparse.ArgumentParser(prog='ctrlcli',
                                                   description='Control '
                                                               'Component '
                                                               'Parser')

        self.ctrl_subparser = self.ctrl_parser.add_subparsers(
            title='Sub Commands',
            description='List of Valid Sub Commands', dest='subparser_name')

        """Sub Parser for all Cli Commands"""
        self.power_parser = self.ctrl_subparser.add_parser('power',
                                                           help='Power on/off/'
                                                                'reset a '
                                                                'device. For '
                                                                'help on POWER,'
                                                                ' use: '
                                                                'python ctrlcli'
                                                                '.py power -h')

        self.resource_parser = self.ctrl_subparser.add_parser('resource',
                                                              help='Resource '
                                                                   'Add'
                                                                   '/Remove'
                                                                   ' from a '
                                                                   'resource '
                                                                   'pool. For '
                                                                   'help on'
                                                                   ' RESOURCE, '
                                                                   ' use: '
                                                                   'python '
                                                                   'ctrlcli.py '
                                                                   'resource -h')

        self.process_parser = self.ctrl_subparser.add_parser('process',
                                                             help='Process '
                                                                  'list/kill on'
                                                                  ' a node in a'
                                                                  ' cluster. '
                                                                  'For help on '
                                                                  'PROCESS use:'
                                                                  ' python '
                                                                  'ctrlcli.py '
                                                                  'process -h')

        self.get_parser = self.ctrl_subparser.add_parser('get',
                                                         help='Get Powercap/'
                                                              'Freq value of a'
                                                              ' node. For help'
                                                              ' on GET, use:'
                                                              ' python ctrlcli.'
                                                              ' py get -h')

        self.set_parser = self.ctrl_subparser.add_parser('set',
                                                         help='Set Powercap/'
                                                              'Freq value of a'
                                                              ' node. For help'
                                                              ' on SET, use:'
                                                              ' python ctrlcli.'
                                                              'py set -h')

    def add_mandatory_args(self):
        """Add the mandatory command line arguments here"""
        self.ctrl_parser.add_argument('device_name',
                                      help='Please provide device name')

    def add_simple_args(self):
        """Add the simple arguments here"""
        self.ctrl_parser.add_argument("-V", "--version", action="version",
                                      version='1.0',
                                      help='Provides the version of the tool')

    def add_power_args(self):
        """Add the arguments for the Power Sub-Parser"""
        self.power_parser.add_argument('subcommand',
                                       choices=['on', 'off', 'cycle'],
                                       help='Select one from three option.s'
                                            ' On/Off/Cycle.'
                                            ' Ex: python ctrlcli.py power on '
                                            'node001')
        self.power_parser.add_argument("-f", "--force", action='store_true',
                                       help='This option will allow user to'
                                            ' force the Power On/Off/Reboot')

    def add_resource_args(self):
        """Add the arguments for the Resource Sub-Parser"""
        self.resource_parser.add_argument('subcommand',
                                          choices=['add', 'remove'],
                                          help='Select one of two options.'
                                               ' Add/Remove.'
                                               ' Ex: python ctrlcli.py resource'
                                               ' add node001')

    def add_process_args(self):
        """Add the arguments for the Process Sub-Parser"""
        self.process_parser.add_argument('subcommand', choices=['list', 'kill'],
                                         help='Select one of two options.'
                                              ' List/Kill. '
                                              ' Ex: python ctrlcli.py resource '
                                              'kill 1232')
        self.process_parser.add_argument('process_id',
                                         help='Please provide process id '
                                              'to list or kill a process')

    def add_get_cmd_args(self):
        """Add the arguments for the Get Sub-Parser"""
        self.get_parser.add_argument('subcommand', choices=['freq', 'powercap'])

    def add_set_cmd_args(self):
        """Add the arguments for the Set Sub-Parser"""
        self.set_parser.add_argument('subcommand', choices=['freq', 'powercap'])
        self.set_parser.add_argument('value',
                                     help='Please provide the value to be set')

    def get_all_args(self):
        """Retrieve all the arguments from parser"""
        self.add_mandatory_args()
        self.add_simple_args()
        self.add_power_args()
        self.add_resource_args()
        self.add_process_args()
        self.add_get_cmd_args()
        self.add_set_cmd_args()
        ctrl_args = self.ctrl_parser.parse_args()
        return ctrl_args


class CtrlCliExecutor(object):
    """This class executes the commands based on user's request"""

    def __init__(self):
        pass

    @classmethod
    def power_cmd_execute(cls, cmd_args):
        """Function to call appropriate power sub-command"""
        if cmd_args.subcommand == 'on':
            retval = \
                CommandExeFactory().power_on_invoker(cmd_args.device_name,
                                                     [cmd_args.subcommand])
            return retval
        elif cmd_args.subcommand == 'off':
            retval = \
                CommandExeFactory().power_off_invoker(cmd_args.device_name,
                                                      [cmd_args.subcommand])
            return retval
        else:
            retval = \
                CommandExeFactory().power_cycle_invoker(cmd_args.device_name,
                                                        [cmd_args.subcommand])
            return retval

    @classmethod
    def process_cmd_execute(cls, cmd_args):
        """Function to call appropriate process sub-command"""
        if cmd_args.subcommand == 'list':
            print"\tProcess List Command called\n" \
                 "\tHowever for this command work is in progress.\n" \
                 "\tSo hold your breath till we develop this module\n"
            return 0
        else:
            print"\tProcess Kill Command Called\n" \
                 "\tHowever for this command work is in progress.\n" \
                 "\tSo hold your breath till we develop this module\n"
            return 0

    @classmethod
    def resource_cmd_execute(cls, cmd_args):
        """Function to call appropriate resource sub-command"""
        if cmd_args.subcommand == 'add':
            retval = \
                CommandExeFactory().power_on_invoker(cmd_args.device_name,
                                                     [cmd_args.subcommand])
            return retval
        else:
            retval = \
                CommandExeFactory().power_on_invoker(cmd_args.device_name,
                                                     [cmd_args.subcommand])
            return retval

    @classmethod
    def get_cmd_execute(cls, cmd_args):
        """Function to call appropriate get sub-command"""
        if cmd_args.subcommand == 'powercap':
            print"\tGet Powercap Command Called\n" \
                 "\tHowever for this command work is in progress.\n" \
                 "\tSo hold your breath till we develop this module\n"
            return 0
        else:
            print"\tGet Freq Command Called\n" \
                 "\tHowever for this command work is in progress.\n" \
                 "\tSo hold your breath till we develop this module\n"
            return 0

    @classmethod
    def set_cmd_execute(cls, cmd_args):
        """Function to call appropriate set sub-command"""
        if cmd_args.subcommand == 'powercap':
            print"\tSet Powercap Command Called\n" \
                 "\tHowever for this command work is in progress.\n" \
                 "\tSo hold your breath till we develop this module\n"
            return 0
        else:
            print"\tSet Freq Command Called\n" \
                 "\tHowever for this command work is in progress.\n" \
                 "\tSo hold your breath till we develop this module\n"
            return 0

    @classmethod
    def execute_cli_cmd(cls):
        """Function to call appropriate sub-parser"""
        masterparser = CtrlCliParser()
        cmd_args = masterparser.get_all_args()
        if cmd_args.subparser_name == 'power':
            cls.power_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'process':
            cls.process_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'resource':
            cls.resource_cmd_execute(cmd_args)
        elif cmd_args.subparser_name == 'get':
            cls.get_cmd_execute(cmd_args)
        else:
            cls.set_cmd_execute(cmd_args)
