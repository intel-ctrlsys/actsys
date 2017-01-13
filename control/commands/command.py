# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Defines the layout of a command object
"""
from ..plugin import PluginManager, DeclareFramework


@DeclareFramework('command')
class Command(object):
    """
    Abstract Base Class for all command objects. Ensure derived objects follow
    its conventions.
    """

    def __init__(self, args):
        """
        Command 'args' are a dictionary of five items listed below:
            'device_name': str: device_name for the command
            'configuration': obj: configuration object
            'plugin_manager': obj: PluginManager instance
            'logger': obj: logger for use in the code base for debug messages
            'arguments': list: command args specific to the command
        """
        if args is None:
            raise RuntimeError('Cannot pass "None" as arguments for commands!')

        self.command_args = args

        if 'device_name' not in args or args['device_name'] is None or len(args['device_name']) == 0:
            raise RuntimeError('The "device_name" argument cannot be missing '
                               'or "None" or an empty string!')
        self.device_name = args['device_name']
        if 'configuration' not in args or args['configuration'] is None:
            raise RuntimeError('The "configuration" argument cannot be missing or "None"!')
        self.configuration = args['configuration']
        if 'plugin_manager' not in args or args['plugin_manager'] is None or \
                not isinstance(args['plugin_manager'], PluginManager):
            raise RuntimeError('The "plugin_manager" argument cannot be '
                               'missing, "None" or a different type!')
        self.plugin_manager = args['plugin_manager']
        if 'logger' in args:
            self.logger = args['logger']
        else:
            self.logger = None
        if 'arguments' in args:
            self.args = args['arguments']
        else:
            self.args = None

    def get_name(self):
        """Get the Class name"""
        if self.__class__.__name__ not in ['_Framework', '_Plugin']:
            return self.__class__.__name__
        if hasattr(self, 'PLUGIN_NAME'):
            return self.PLUGIN_NAME
        elif hasattr(self, 'FRAMEWORK_NAME'):
            return self.FRAMEWORK_NAME

    def execute(self):
        """How the command is performed; default returns unknown error."""
        return CommandResult()


class CommandResult(object):
    """How the result of commands is stored."""

    def __init__(self, return_code=-1, message="Unknown Error", device_name=None):
        """Construct a command result object."""
        self.return_code = return_code
        self.message = message
        self.device_name = device_name

    def __str__(self):
        if self.device_name is None:
            return "{} - {}".format(self.return_code, self.message)
        else:
            return "{}: {} - {}".format(self.device_name, self.return_code, self.message)
