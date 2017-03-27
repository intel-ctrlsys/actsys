# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
CLI commands specificly for provisioning. Putting it in it's own class/file like this allows the Provisioning CLI to be
used sperately from control. If desired.
"""
from __future__ import print_function
import argparse
from ..commands import CommandResult


class ProvisionCli(object):
    """
    A CLI for provisioning.
    """

    def __init__(self, command_invoker):
        self.command_invoker = command_invoker
        self.root_parser = argparse.ArgumentParser(prog='provision')

        self.subparsers = self.root_parser.add_subparsers(title='Action',
                                                          description='What do you want the provisioner to do?')
        self.add_add_args()
        self.add_delete_args()
        self.add_set_args()

    def add_add_args(self):
        """

        :return:
        """
        self.add_parser = self.subparsers.add_parser('add', help='Add a device to the provisioner')
        self.add_parser.add_argument('device_name', help="The device name of the device you want to add.")
        self.add_parser.set_defaults(execute_function=self.add_execute)

    def add_delete_args(self):
        """

        :return:
        """
        self.delete_parser = self.subparsers.add_parser('delete', help='Delete a device from the provisioner')
        self.delete_parser.add_argument('device_name', help="The name of the device you want to delete.")
        self.delete_parser.set_defaults(execute_function=self.delete_execute)

    def add_set_args(self):
        """
        Add the arguments under the pattern `provisioner device ...`
        :return:
        """
        self.set_parser = self.subparsers.add_parser('set', description="Manage devices by setting options to them.",
                                                     help='Manage devices properties for the provisioner')
        self.set_parser.add_argument('device_name', help="The device name of the device you want to add")
        self.set_parser.add_argument('--ip_address', '-i', type=str, required=False,
                                     help="The IP address you want to set. This is set on the interface specified with"
                                          " the --net_interface flag. If no value is given, then no"
                                          "change takes place. Set this field to UNDEF to remove the currently "
                                          "specified IP address.")
        self.set_parser.add_argument('--hw_address', '-a', type=str, required=False,
                                     help="The Hardware address of this device. This is set for the interface specified"
                                          " with the --net_interface flag. If no value is given, then no"
                                          "change takes place. Set this field to UNDEF to remove the currently "
                                          "specified hardware address.")
        self.set_parser.add_argument('--net_interface', '-d', type=str, required=False,
                                     help="The network interface which you want to set the options on. This applies to"
                                          " the --ip_address and --hw_address flags. If no network interface is "
                                          "supplied, it defaults to eth0.")
        self.set_parser.add_argument('--image', '-m', type=str, required=False,
                                     help="The image you want to set to this node. If no value is given, then no image "
                                          "is set. The image should already be defined and known to the provisioner and"
                                          "only the image name is specified here.")
        self.set_parser.add_argument('--bootstrap', '-b', type=str, required=False,
                                     help="The bootstrap to be used by the provisioner. The existance and use of a "
                                          "bootstrap image depends on the provisioner. If no value is given, then no"
                                          "change takes place. Set this field to UNDEF to remove the currently "
                                          "specified bootstrap.")
        self.set_parser.add_argument('--files', '-f', type=str, required=False,
                                     help="The files you want to set on this device. This should be a comma seperated "
                                          "list if you are specifying multiple files. If no value is given, then no"
                                          "change takes place. Set this field to UNDEF to remove all existing files.")
        self.set_parser.add_argument('--kernel_args', '-k', type=str, required=False,
                                     help="The kernel arguments to set on this device. This should be in the same "
                                          "format you want to show up in the kernel arguments. If no value is given, "
                                          "then no change takes place. Set this field to UNDEF to remove all existing "
                                          "kernel arguments.")
        self.set_parser.set_defaults(execute_function=self.set_execute)

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

    def add_execute(self, parsed_args):
        """
        Execute Add commands
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        print("Adding a device with args: {}".format(parsed_args))
        return self.command_invoker.provision_add(parsed_args.device_name, parsed_args)

    def delete_execute(self, parsed_args):
        """
        Execute delete commands
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        print("Deleting with args: {}".format(parsed_args))
        return self.command_invoker.provision_delete(parsed_args.device_name, parsed_args)

    def set_execute(self, parsed_args):
        """
        Execute set commands
        :param parsed_args: As defined by the CLI above
        :return: CommandResult
        """
        print("Set with args: {}".format(parsed_args))
        return self.command_invoker.provision_set(parsed_args.device_name, parsed_args)
