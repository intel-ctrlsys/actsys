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
                                                          description='What kind of diagnostic tests (in-band/out-of-band)'
                                                                      ' do you want to run?')
        self.add_inband_args()
        self.add_oob_args()

    def add_inband_args(self):
        """

        :return:
        """
        self.inband_parser = self.subparsers.add_parser('inband', help='Launch the in band diagnostic tests. Ex.: ctrl diag inband '
                                                                      'test_device --image test_image --test test_tests')
        self.inband_parser.add_argument('device_name', help="The device name of the device you want to launch diagnostics on.")
        self.inband_parser.add_argument('--image', type=str, required=True, help="The diagnostics image to be used.")
        self.inband_parser.add_argument('--test', type=str, required=False, help="The specific diagnostic tests you "
                                        "wish to launch. This input is passed to the Kernel args used while "
                                        "provisioning, please refer to user guide to provide the options correctly.")
        self.inband_parser.set_defaults(execute_function=self.inband_execute)

    def add_oob_args(self):
        """

        :return:
        """
        self.oob_parser = self.subparsers.add_parser('oob', help='Launch the out-of-band diagnostic tests. Ex.: ctrl diag oob '
                                                                      'test_device --test test_tests')
        self.oob_parser.add_argument('device_name', help="The device name of the device you want to launch diagnostics on.")
        self.oob_parser.add_argument('--test', type=str, required=False, help="The specific diagnostic tests you wish to launch.(Ex. IFST/Ping)")
        self.oob_parser.set_defaults(execute_function=self.oob_execute)

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

    def inband_execute(self, parsed_args):
        """
        Execute inband commands
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.diagnostics_inband(parsed_args.device_name, parsed_args.test, parsed_args.image)

    def oob_execute(self, parsed_args):
        """
        Execute oob commands
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.diagnostics_oob(parsed_args.device_name, parsed_args.test)

