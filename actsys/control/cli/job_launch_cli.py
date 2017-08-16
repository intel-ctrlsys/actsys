# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
CLI commands specifically for job launch component.
"""
import argparse
from ..commands import CommandResult


class JobLaunchCli(object):
    """
    A CLI for job launch.
    """

    def __init__(self, command_invoker):
        self.command_invoker = command_invoker
        self.root_parser = argparse.ArgumentParser(prog='job')

        self.subparsers = self.root_parser.add_subparsers(title='Action',
                                                          description='What to do with job '
                                                                      '(launch/check/retrieve/cancel)?')
        self.add_launch_args()
        self.add_check_args()
        self.add_retrieve_args()
        self.add_cancel_args()

    def add_launch_args(self):
        """

        :return:
        """
        self.add_parser = self.subparsers.add_parser('launch',
                                                     help='launch a batch job.')
        self.add_parser.add_argument('job_script',
                                     help='The batch job script to be launched.')
        self.add_parser.add_argument('--node_count', '-N', required=False,
                                     help='Number of nodes required.')
        self.add_parser.add_argument('--nodes', '-n', required=False,
                                     help='The list of nodes required.')
        self.add_parser.add_argument('--output_file', '-o', required=False,
                                     help='The output file to put the job results.')
        self.add_parser.set_defaults(execute_function=self.launch_execute)

    def add_check_args(self):
        """

        :return:
        """
        self.check_parser = self.subparsers.add_parser('check',
                                                       help='check job metadata.')
        self.check_parser.add_argument('--job_id', '-j', required=False,
                                       help='The job id to be checked.')
        self.check_parser.add_argument('--state', '-s', required=False,
                                       help='Check jobs with certain state.')
        self.check_parser.set_defaults(execute_function=self.check_execute)

    def add_retrieve_args(self):
        """
        Retrieve job output
        :return:
        """
        self.retrieve_parser = self.subparsers.add_parser('retrieve',
                                                          help='Retrieve job output.')
        self.retrieve_parser.add_argument('job_id',
                                          help='The job id to be retrieved.')
        self.retrieve_parser.add_argument('--output_file', '-o', required=False,
                                          help='The output file from which to retrieve job result.')
        self.retrieve_parser.set_defaults(execute_function=self.retrieve_execute)

    def add_cancel_args(self):
        """
        Cancel job
        :return:
        """
        self.cancel_parser = self.subparsers.add_parser('cancel',
                                                        help='cancel a job.')
        self.cancel_parser.add_argument('job_id',
                                        help='The job id to be cancelled.')
        self.cancel_parser.set_defaults(execute_function=self.cancel_execute)

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
            return CommandResult(1, exception)

    def launch_execute(self, parsed_args):
        """
        Execute job launch command
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.job_launch(parsed_args.job_script,
                                               parsed_args.node_count,
                                               parsed_args.nodes,
                                               parsed_args.output_file)

    def check_execute(self, parsed_args):
        """
        Execute job check command
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.job_check(parsed_args.job_id,
                                              parsed_args.state)

    def retrieve_execute(self, parsed_args):
        """
        Execute job retrieve command
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.job_retrieve(parsed_args.job_id,
                                                 parsed_args.output_file)

    def cancel_execute(self, parsed_args):
        """
        Execute job cancel command
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        return self.command_invoker.job_cancel(parsed_args.job_id)