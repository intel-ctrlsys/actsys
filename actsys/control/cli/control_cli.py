# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright (c) 2016 Intel Corp.
#
"""
This module creates the command line parser and executes the user commands.
"""



import argparse
import sys
import os
import logging
import timeout_decorator
from datastore.datastore_cli import DataStoreCLI
from .command_invoker import CommandInvoker
from ..commands import CommandResult, ConfigurationNeeded
from .provision_cli import ProvisionCli
from .diagnostics_cli import DiagnosticsCli
from .job_launch_cli import JobLaunchCli
from sys import argv, exit, stderr
from IPython import start_ipython
from IPython.terminal.prompts import Token, Prompts
from traitlets.config.loader import Config


class InitPrompt(Prompts):
    """Custom Prompt, makes the default prompt Ctrl[i]"""
    def in_prompt_tokens(self, cli=None):
        return[(Token.Prompt, 'Ctrl ['),
               (Token.PromptNum, str(self.shell.execution_count)),
               (Token.Prompt, ']: ')]


class InteractiveCli(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None):
        argparse.Action.__init__(self, option_strings=option_strings, dest=dest, nargs=nargs, const=const, default=default, type=type, choices=choices, required=required, help=help, metavar=metavar)

    def __call__(self, *args, **kwargs):
        print ("........Initializing Interactive cli........")
        cfg = Config()
        cfg.IPCompleter.merge_completions = False
        cfg.TerminalInteractiveShell.prompts_class = InitPrompt
        cfg.InteractiveShellApp.exec_lines = ['import control.cli.interactive_commands\n']
        cfg.TerminalInteractiveShell.banner1 = '\x1b[2J\x1b[H\n' \
                                               '*************************************************************\n' \
                                               'ActSys via IPython Shell'
        cfg.TerminalInteractiveShell.banner2 = '\nActSys specific commands you can use are:\n' \
                                               '\tpower     Power on/off/cycle\n' \
                                               '\tresource  Add or remove resource from resource pool\n' \
                           '\tprocess   Process list/kill on a node in a cluster\n' \
                           '\tget       Get powercap/freq value of a node\n' \
                           '\tset       Set powercap/freq value of a node\n' \
                           '\tservice   Check, start or stop services specified in the configuration file\n' \
                           '\tprovision Adding, setting and removing provisioning options for devices\n' \
                           '\tdiag      Launching diagnostic tests on devices\n' \
                           '\tbios      Update or get version of bios on specified nodes/group\n' \
                           '\tsensor    Get specifiged sensor value on specified nodes/group\n' \
                           '\tjob       Launch, check, retrive or cancel job\n' \
                           '\nInteractive cli commands to select/clear nodes are:\n' \
                           '\tselect          Select node or group\n' \
                           '\tclear_select    Clear selection. Provide device name for each command\n' \
                                               'For help on these commands type <command_name>?. For example to get\n' \
                                               'help on power type "power?" and enter it.Type menu to see command list\n'
        start_ipython(argv=argv[1:], config=cfg)
        exit(0)


class ControlArgParser(object):
    """Control Parser Class"""

    CLI_COMMAND = "ctrl"

    def __init__(self):
        """Init Function for Control Cli Parser"""
        self.CLI_COMMAND = os.path.basename(sys.argv[0])

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

        self.ctrl_subparser.add_parser('datastore', help="Raw access to the database and its contects", add_help=False)
        self.ctrl_subparser.add_parser('cmm', help="Configuration Manifest Management (CMM) is a user friendly way to update your configuration.", add_help=False)
        self.ctrl_subparser.add_parser('provision', help="Adding, setting and removing provisioning "
                                                         "options for devices", add_help=False)
        self.ctrl_subparser.add_parser('diag', help="Launching diagnostic tests on devices", add_help=False)

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

        self.add_subparser('sensor', 'Get specified sensor value on specified nodes/group of nodes',
                           ['get'], 'Select option to get sensor values'
                                    'Ex: 1. {0} sensor-name temp 2. {1} sensor-name temp --get-overtime 2 3'.
                           format(self.CLI_COMMAND, self.CLI_COMMAND),
                           [
                               {
                                   'name': 'sensor_name',
                                   'nargs': '?',
                                   'help': 'Provide a specific sensor, a comma seperated list of multiple sensors '
                                           'or "*" for all sensors'
                               },
                               {
                                   'name': '--get-overtime',
                                   'nargs': 2,
                                   'type': int,
                                   'metavar': ('<sample-rate>', '<duration>'),
                                   'help': 'Provide a sample rate(per second) and a duration of time(seconds) to sample'
                                           ' over, both values must be integers greater than 1'
                               }
                           ])
        self.ctrl_subparser.add_parser('job', help='Launching, checking, '
                                                   'retrieving and canceling job', add_help=False)

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
        self.ctrl_parser.add_argument("-v", "--verbosity", action="count", help="increase output verbosity")
        self.ctrl_parser.add_argument("-i", action=InteractiveCli, nargs=0, help="Start in interactive mode")
        self.ctrl_parser.add_argument("-t", "--timeout", type=float,
                                      help="Provides a timeout for the command")

    def get_all_args(self, args=None):
        if len(sys.argv) == 1:
            self.ctrl_parser.print_help()
            sys.exit(1)
        return self.ctrl_parser.parse_args(args)


class ControlCommandLineInterface(object):
    """This class executes the commands based on user's request"""
    def __init__(self):
        self.cmd_invoker = None
        """default timeout value is 30 minutes"""
        self.default_timeout = 1800
        self.timeout = 0

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

    def oobsensor_cmd_execute(self, cmd_args):
        if cmd_args.subcommand == 'get':
            if cmd_args.get_overtime is None:
                return self.cmd_invoker.oob_sensor_get(cmd_args.device_name, cmd_args.sensor_name)
            else:
                sample_rate = cmd_args.get_overtime[0]
                duration = cmd_args.get_overtime[1]
                return self.cmd_invoker.oob_sensor_get_over_time(cmd_args.device_name, cmd_args.sensor_name, duration,
                                                                 sample_rate)
        else:
            return CommandResult(1, "Invalid sensor command entered")

    def _execute_local_command(self, local_cmd_args):
        """Check and run the corresponding command"""
        command_result = None
        if local_cmd_args.subparser_name == 'power':
            command_result = self.power_cmd_execute(local_cmd_args)
        elif local_cmd_args.subparser_name == 'process':
            command_result = self.process_cmd_execute(local_cmd_args)
        elif local_cmd_args.subparser_name == 'resource':
            command_result = self.resource_cmd_execute(local_cmd_args)
        elif local_cmd_args.subparser_name == 'get':
            command_result = self.get_cmd_execute(local_cmd_args)
        elif local_cmd_args.subparser_name == 'set':
            command_result = self.set_cmd_execute(local_cmd_args)
        elif local_cmd_args.subparser_name == 'service':
            command_result = self.service_cmd_execute(local_cmd_args)
        elif local_cmd_args.subparser_name == 'bios':
            command_result = self.bios_cmd_execute(local_cmd_args)
        elif local_cmd_args.subparser_name == 'sensor':
            command_result = self.oobsensor_cmd_execute(local_cmd_args)
        return command_result

    def handle_invalid_timeout(self, message):
        message += ' Keep executing the command with the default timeout:' + \
                   str(self.default_timeout)
        self.cmd_invoker.logger.warning(message)
        self.timeout = self.default_timeout

    def execute_cmd(self, cmd_args, masterparser, unknown_args):
        """Execute the command through an internal function with
        timeout decorator that uses specified timeout value"""
        try:
            self.set_time_out(cmd_args)
        except (ConfigurationNeeded, ValueError) as error:
            self.handle_invalid_timeout(str(error))
        if self.timeout < 0:
            self.handle_invalid_timeout('Timeout value (' + str(self.timeout) +
                                        ') should not be negative!')

        @timeout_decorator.timeout(self.timeout)
        def execute_cmd_internal():
            try:
                if cmd_args.subparser_name == 'datastore':
                    datastore_cli = DataStoreCLI(self.cmd_invoker.get_datastore()).\
                        parse_and_run(unknown_args)
                    return datastore_cli
                if cmd_args.subparser_name == 'provision':
                    provisioner_result = ProvisionCli(self.cmd_invoker).parse_and_run(
                        unknown_args)
                    return self.handle_command_result(provisioner_result)
                if cmd_args.subparser_name == 'cmm':
                    return self.cmd_invoker.launch_cmm()
                if cmd_args.subparser_name == 'diag':
                    diagnostic_result = DiagnosticsCli(self.cmd_invoker).parse_and_run(unknown_args)
                    return self.handle_command_result(diagnostic_result)
                if cmd_args.subparser_name == 'job':
                    job_result = JobLaunchCli(self.cmd_invoker).parse_and_run(unknown_args)
                    return self.handle_command_result(job_result)
                command_result = self._execute_local_command(masterparser.get_all_args())

            except timeout_decorator.TimeoutError:
                """TODO to kill all the sub processes!"""
                command_result = CommandResult(-1, 'The command timed out '
                                                   'before done!')

            return self.handle_command_result(command_result)

        return execute_cmd_internal()

    def get_cmd_invoker_args(self, verbosity):
        """Set the screen log level according to verbosity"""
        cmd_invoker_args = dict()
        if verbosity == 1:
            cmd_invoker_args["screen_log_level"] = logging.INFO
        elif verbosity == 2:
            cmd_invoker_args["screen_log_level"] = logging.DEBUG
        return cmd_invoker_args

    def set_time_out(self, cmd_args):
        """Set the timeout value, either from the command line or from
        the configuration file"""
        if cmd_args.timeout is not None:
            self.timeout = cmd_args.timeout
        else:
            cmd_timeout = self.cmd_invoker.get_datastore().\
                get_configuration_value('cmd_timeout')
            if cmd_timeout is not None:
                try:
                    self.timeout = float(cmd_timeout)
                except ValueError as value_error:
                    raise value_error
            else:
                raise ConfigurationNeeded('cmd_timeout')

    def execute_cli_cmd(self):
        """Function to call appropriate sub-parser"""
        masterparser = ControlArgParser()
        cmd_args, unknown_args = masterparser.ctrl_parser.parse_known_args()
        cmd_invoker_args = self.get_cmd_invoker_args(cmd_args.verbosity)
        try:
            self.cmd_invoker = CommandInvoker(**cmd_invoker_args)
        except Exception as f:
            if hasattr(f, 'value'):
                print(f.value)
            else:
                print(f)
            sys.exit(1)
        return self.execute_cmd(cmd_args, masterparser, unknown_args)

    def handle_command_result(self, command_result):
        """

        :param command_result:
        :return:
        """
        if isinstance(command_result, list):
            num_device = 0
            num_failed_device = 0
            num_failures = 0
            for cr in command_result:
                count = len(self.cmd_invoker.datastore.
                            expand_device_list(cr.device_name))
                num_device += count
                if cr.return_code != 0:
                    print(cr, file=sys.stderr)
                    num_failed_device += count
                    num_failures += 1
                else:
                    print(cr)
            print("Result: {}/{} devices were successful".
                  format(num_device - num_failed_device, num_device))
            return num_failures
        else:
            if command_result.return_code != 0:
                print(command_result, file=sys.stderr)
            else:
                print(command_result)
            return command_result.return_code
