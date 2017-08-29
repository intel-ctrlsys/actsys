# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright (c) 2017 Intel Corp.
#
"""
This module creates the interactive command line parser and executes commands.
"""

from IPython.core.magic import (Magics, magics_class, line_magic)
from IPython import get_ipython
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)
from IPython.core.completerlib import quick_completer
from IPython.terminal.prompts import Prompts, Token
from .command_invoker import CommandInvoker

class CustomPrompt(Prompts):
    """Custom Prompt, this prompt changes with the nodes being set"""
    def in_prompt_tokens(self, cli=None):
        line_number = self.shell.execution_count - CtrlCommands.curLine
        return [(Token.Prompt, CtrlCommands.NODES + ' ['),
                (Token.PromptNum, str(line_number)),
                (Token.Prompt, ']: ')]


class CtrlPrompt(Prompts):
    """Custom Prompt, makes the default prompt Ctrl[i]"""
    def in_prompt_tokens(self, cli=None):
        line_number = CtrlCommands.ctrlLine + (self.shell.execution_count - CtrlCommands.curLine)
        return[(Token.Prompt, 'Ctrl ['),
               (Token.PromptNum, str(line_number)),
               (Token.Prompt, ']: ')]

@magics_class
class CtrlCommands(Magics):
    """All the Ctrl Commands"""
    NODES = None
    curLine = 0
    ctrlLine = 0
    ctrlPrompt = True

    def __init__(self, shell):
        # Constructor for UserMagics class. Get the instance of ASD class
        super(CtrlCommands, self).__init__()
        self.add_completer_options()
        self.ctrl_command_invoker = CommandInvoker()
        self.device_name = None
        CtrlCommands.curLine = 0
        CtrlCommands.ctrlLine = 0
        CtrlCommands.ctrlPrompt = True

    @line_magic
    @magic_arguments()
    @argument('node_regex', help='Set nodes to be used for all commands.'
                                 'Use "clear_selection" to unset')
    def select(self, args):
        """Set node regex"""
        parse_args = parse_argstring(CtrlCommands.select, args)
        if self.check_valid_devices(parse_args.node_regex, self):
            CtrlCommands.NODES = parse_args.node_regex
        else:
            return
        ipy = get_ipython()
        if CtrlCommands.ctrlPrompt:
            CtrlCommands.ctrlLine = ipy.execution_count
        CtrlCommands.ctrlPrompt = False
        CtrlCommands.curLine = ipy.execution_count
        ipy.prompts = CustomPrompt(ipy)

    @staticmethod
    @line_magic
    def clear_select(self):
        """Return to default prompt"""
        CtrlCommands.NODES = None
        CtrlCommands.ctrlPrompt = True
        ipy = get_ipython()
        CtrlCommands.curLine = ipy.execution_count
        ipy.prompts = CtrlPrompt(ipy)

    @line_magic
    @magic_arguments()
    @argument('subcommand', help='on, off, cycle, bios, efi, hdd, pxe, cdrom, removable',
              choices=('on', 'off', 'cycle', 'bios', 'efi', 'hdd', 'pxe', 'cdrom', 'removable'))
    @argument('-o', '--outlet', help='Power off with pdu outlet')
    @argument('-d', '--device', help='Device name. Required if nodename is not set')
    @argument('-f', '--force', help='This option will allow user to force thePower On/Off/Reboot')
    def power(self, args):
        """Power management commands """
        parse_args = parse_argstring(CtrlCommands.power, args)
        command_result = self.ctrl_command_invoker.common_cmd_invoker(
            self.get_device(parse_args), parse_args.subcommand)
        self.handle_command_result(self, command_result)


    @line_magic
    @magic_arguments()
    @argument('action', help='add or remove',
              choices=('add', 'remove', 'check'))
    @argument('-d', '--device', help='Device name. Required if nodename is not set')
    def resource(self, args):
        """Resource management commands"""
        parse_args = parse_argstring(CtrlCommands.resource, args)
        if parse_args.action == 'add':
            command_result = self.ctrl_command_invoker.resource_add(
                self.get_device(parse_args))
        elif parse_args.action == 'remove':
            command_result = self.ctrl_command_invoker.resource_remove(
                self.get_device(parse_args))
        elif parse_args.action == 'check':
            command_result = self.ctrl_command_invoker.resource_check(
                self.get_device(parse_args))
        return self.handle_command_result(self, command_result)


    @line_magic
    @magic_arguments()
    @argument('action', help='status, start, stop', choices=('status', 'start', 'stop'))
    @argument('-d', '--device', help='Device name. Required if nodename is not set')
    def service(self, args):
        """Service management commands """
        parse_args = parse_argstring(CtrlCommands.service, args)
        if parse_args.action == 'status':
            command_result = self.ctrl_command_invoker.service_status(
                self.get_device(parse_args))
        elif parse_args.action == 'start':
            command_result = self.ctrl_command_invoker.service_on(
                self.get_device(parse_args))
        elif parse_args.action == 'stop':
            command_result = self.ctrl_command_invoker.service_off(
                self.get_device(parse_args))
        self.handle_command_result(self, command_result)


    @line_magic
    @magic_arguments()
    @argument('action', help='add, delete, set', choices=('add', 'delete', 'set'))
    @argument('-d', '--device', help='Device name. Required if nodename is not set')
    @argument('-ip', '--ip-address', help='IP address')
    @argument('-hw', '--hw-address', help='hw address')
    @argument('-n', '--net-interface', help='net interface')
    @argument('-i', '--image', help='image')
    @argument('-b', '--bootstrap', help='bootstrap')
    @argument('-f', '--file', help='file')
    @argument('-k', '--kernel-args', help='kernel args')
    def provision(self, args):
        """Provision management commands """
        parse_args = parse_argstring(CtrlCommands.provision, args)
        if parse_args.action == 'add':
            command_result = self.ctrl_command_invoker.provision_add(
                self.get_device(parse_args))
        elif parse_args.action == 'delete':
            command_result = self.ctrl_command_invoker.provision_delete(
                self.get_device(parse_args))
        elif parse_args.action == 'set':
            command_result = self.ctrl_command_invoker.provision_set(
                self.get_device(parse_args))
        self.handle_command_result(self, command_result)


    @line_magic
    @magic_arguments()
    @argument('action', help='inband or oob', choices=('inband', 'oob'))
    @argument('-d', '--device', help='Device name. Required if nodename is not set')
    @argument('-t', '--test', help='Test name')
    @argument('-i', '--image', help='Image')
    def diag(self, args):
        """Diag management commands """
        parse_args = parse_argstring(CtrlCommands.diag, args)
        if parse_args.action == 'inband':
            command_result = self.ctrl_command_invoker.diagnostics_inband(
                self.get_device(parse_args))
        elif parse_args.action == 'oob':
            command_result = self.ctrl_command_invoker.diagnostics_oob(
                self.get_device(parse_args))
        self.handle_command_result(self, command_result)


    @line_magic
    @magic_arguments()
    @argument('subcommand', help='update or get-version', choices=('update', 'get-version'))
    @argument('-d', '--device', help='Device name. Required if nodename is not set')
    @argument('-i', '--image', help='Specify the bios image')
    def bios(self, args):
        """Bios management commands """
        parse_args = parse_argstring(CtrlCommands.bios, args)
        command_result = self.ctrl_command_invoker.common_cmd_invoker(
            self.get_device(parse_args), parse_args.subcommand)
        self.handle_command_result(self, command_result)


    @line_magic
    @magic_arguments()
    @argument('subcommand', help='get or get over time', choices=('get', 'get_over_time'))
    @argument('-s', '--sensor-name', help='Sensor name required')
    @argument('-d', '--device', help='Device name. Required if nodename is not set')
    def sensor(self, args):
        """Sensor management commands """
        parse_args = parse_argstring(CtrlCommands.sensor, args)
        command_result = self.ctrl_command_invoker.common_cmd_invoker(
            self.get_device(parse_args), parse_args.subcommand)
        self.handle_command_result(self, command_result)


    @line_magic
    @magic_arguments()
    @argument('subcommand', help='launch, check, retrieve, cancel', choices=('launch', 'check', 'retrieve', 'cancel'))
    @argument('-j', '--job_id', help='Job ID required')
    @argument('-nc', '--node-count', help='node count')
    @argument('-n', '--node', help='node')
    @argument('-o', '--output-file', help='output file')
    @argument('-s-', '--state', help='state')
    def job(self, args):
        """Job management commands"""
        parse_args = parse_argstring(CtrlCommands.job, args)
        command_result = self.ctrl_command_invoker.common_cmd_invoker(
            parse_args, parse_args.subcommand)
        self.handle_command_result(self, command_result)


    @staticmethod
    def get_device(parse_args):
        """Gets the device name"""
        if parse_args.device:
            return parse_args.device
        else:
            return CtrlCommands.NODES

    @staticmethod
    def handle_command_result(self, command_result):
        """Handles the command result"""
        if isinstance(command_result, list):
            num_device = 0
            num_failed_device = 0
            num_failures = 0
            for com_result in command_result:
                count = len(self.ctrl_command_invoker.datastore.
                            expand_device_list(com_result.device_name))
                num_device += count
                if com_result.return_code != 0:
                    num_failed_device += count
                    num_failures += 1
                    print(com_result)
                else:
                    print(com_result)
            print(("Result: {}/{} devices were successful".
                  format(num_device - num_failed_device, num_device)))
        else:
            print (command_result)

    @staticmethod
    def check_valid_devices(device_regex, self):
        valid = True
        try:
            device_list = self.ctrl_command_invoker.datastore.expand_device_list(device_regex)
        except self.ctrl_command_invoker.datastore.DeviceListParseError:
            print("Error parsing device list")
            return False
        if not device_list:
            print("No valid devices to run this command on.")
            return False
        for device_name in device_list:
            if not self.ctrl_command_invoker.device_exists_in_config(device_name):
                print(("{} device does not exist in config.".format(device_name)))
                valid = False
        return valid


    def add_completer_options(self):
        """Sets the tab completion for the options of each command"""
        self.complete_command_option('power', ['on', 'off', 'cycle', 'bios', 'efi', 'hdd', 'pxe', 'cdrom', 'removable'])
        self.complete_command_option('resource', ['remove', 'add', 'check'])
        self.complete_command_option('service', ['status', 'start', 'stop'])
        self.complete_command_option('provision', ['add', 'delete', 'set'])
        self.complete_command_option('diag', ['inband', 'oob'])
        self.complete_command_option('bios', ['update', 'get-version'])
        self.complete_command_option('sensor', ['get', 'get_over_time'])
        self.complete_command_option('job', ['launch', 'check', 'retrieve', 'cancel'])

    @staticmethod
    def complete_command_option(command, options):
        """Sets tab completetion for the commands"""
        quick_completer(command, options)
        quick_completer('%'+command, options)

try:
    IPYTHON_ID = get_ipython()
    MAGICS = CtrlCommands(IPYTHON_ID)
    IPYTHON_ID.register_magics(MAGICS)
except AttributeError:
    print ("Unable to get the IPython shell identifier")

