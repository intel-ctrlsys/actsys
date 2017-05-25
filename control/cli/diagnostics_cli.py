# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
CLI commands specifically for diagnostics.
"""
from __future__ import print_function
import argparse
from ..commands import CommandResult


class DiagnosticsCli(object):
    """
    A CLI for diagnostics.
    """

    def __init__(self, command_invoker):
        self.command_invoker = command_invoker
        self.root_parser = argparse.ArgumentParser(prog='diag')

        self.subparsers = self.root_parser.add_subparsers(title='Action',
                                                          description='What kind of diagnostic tests (online/offline)'
                                                                      ' do you want to run?')
        self.add_online_args()
        self.add_offline_args()

    def add_online_args(self):
        """

        :return:
        """
        self.online_parser = self.subparsers.add_parser('online', help='Launch the online diagnostic tests. Ex.: ctrl diag online '
                                                                      'test_device --image test_image --test test_tests')
        self.online_parser.add_argument('device_name', help="The device name of the device you want to launch diagnostics on.")
        self.online_parser.add_argument('--image', type=str, required=False, help="The diagnostics image to be used.")
        self.online_parser.add_argument('--test', type=str, required=False, help="The specific diagnostic tests you wish to launch.")
        self.online_parser.set_defaults(execute_function=self.online_execute)

    def add_offline_args(self):
        """

        :return:
        """
        self.offline_parser = self.subparsers.add_parser('offline', help='Launch the offline diagnostic tests. Ex.: ctrl diag offline '
                                                                      'test_device --test test_tests')
        self.offline_parser.add_argument('device_name', help="The device name of the device you want to launch diagnostics on.")
        self.offline_parser.add_argument('--test', type=str, required=False, help="The specific diagnostic tests you wish to launch.(Ex. IFST/Ping)")
        self.offline_parser.set_defaults(execute_function=self.offline_execute)

    def parse_and_run(self, args=None):
        """
        Parse the arguments and perform the proper action.
        :param args: Either passed in or retrieved from sys.argv
        :return:
        """
        if args is None:
            args = self.root_parser.parse_args()
        else:
            args = self.root_parser.parse_args(args)
        try:
            return args.execute_function(args)
        except Exception as exception:
            self.root_parser.print_usage()
            print(type(exception), exception.message)
            return CommandResult(1, exception)

    def online_execute(self, parsed_args):
        """
        Execute online commands
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.diagnostics_online(parsed_args.device_name, parsed_args.test, parsed_args.image)

    def offline_execute(self, parsed_args):
        """
        Execute offline commands
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.diagnostics_offline(parsed_args.device_name, parsed_args.test)

