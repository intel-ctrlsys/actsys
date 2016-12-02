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

        """Sub Parser for all Cli Commands"""
        self.power_parser = self.ctrl_subparser.add_parser('power', help='Power on/off/reset a device.')

        self.resource_parser = self.ctrl_subparser.add_parser('resource',
                                                              help='Resource add/remove from a resource pool.')

        self.process_parser = self.ctrl_subparser.add_parser('process',
                                                             help='Process list/kill on a node in a cluster. ')

        self.get_parser = self.ctrl_subparser.add_parser('get',
                                                         help='Get powercap/freq value of a node.')

        self.set_parser = self.ctrl_subparser.add_parser('set',
                                                         help='Set powercap/freq value of a node.')

        self.service_parser = self.ctrl_subparser.add_parser('service',
                                                             help='check, start or stop services specified in'
                                                                  'the configuration file')
        self.add_all_args()


    def add_mandatory_args(self):
        """Add the mandatory command line arguments here"""
        self.ctrl_parser.add_argument('device_name', help='Please provide device name')

    def add_simple_args(self):
        """Add the simple arguments here"""
        self.ctrl_parser.add_argument("-V", "--version", action="version",
                                      version='1.0',
                                      help='Provides the version of the tool')

    def add_power_args(self):
        """Add the arguments for the Power Sub-Parser"""
        self.power_parser.add_argument('subcommand',
                                       choices=['on', 'off', 'cycle', 'bios',
                                                'efi', 'hdd', 'pxe', 'cdrom',
                                                'removable'],
                                       help='Select an option: on/off/cycle/bios/efi/hdd/pxe/cdrom/removable.'
                                            ' Ex: {} power on node001'.format(self.CLI_COMMAND))
        self.power_parser.add_argument("-f", "--force", action='store_true',
                                       help='This option will allow user to'
                                            ' force the Power On/Off/Reboot')

    def add_resource_args(self):
        """Add the arguments for the Resource Sub-Parser"""
        self.resource_parser.add_argument('subcommand',
                                          choices=['add', 'remove', 'check'],
                                          help='Select one of the following options: add/remove/check'
                                               ' Ex: {} resource add node001'.format(self.CLI_COMMAND))

    def add_process_args(self):
        """Add the arguments for the Process Sub-Parser"""
        self.process_parser.add_argument('subcommand', choices=['list', 'kill'],
                                         help='Select one of two options: list/kill. '
                                              ' Ex: {} resource kill 1232'.format(self.CLI_COMMAND))
        self.process_parser.add_argument('process_id',
                                         help='Please provide process id to list or kill a process')

    def add_get_cmd_args(self):
        """Add the arguments for the Get Sub-Parser"""
        self.get_parser.add_argument('subcommand', choices=['freq', 'powercap'])

    def add_set_cmd_args(self):
        """Add the arguments for the Set Sub-Parser"""
        self.set_parser.add_argument('subcommand', choices=['freq', 'powercap'])
        self.set_parser.add_argument('value',
                                     help='Please provide the value to be set')

    def add_service_args(self):
        """Add service args"""
        self.service_parser.add_argument('subcommand', choices=['status', 'start', 'stop'])

    def add_all_args(self):
        """Retrieve all the arguments from parser"""
        self.add_mandatory_args()
        self.add_simple_args()
        self.add_power_args()
        self.add_resource_args()
        self.add_process_args()
        self.add_get_cmd_args()
        self.add_set_cmd_args()
        self.add_service_args()

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
            raise RuntimeError("A runtime error occurred, exiting abnormally.")

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
            print ("Invalid service command entered.")
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