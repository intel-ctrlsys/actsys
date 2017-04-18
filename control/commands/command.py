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

    def __init__(self, device_name, configuration, plugin_manager, logger=None, **additional_arguments):
        """

        :param device_name: str: device_name for the command
        :param configuration: obj: configuration object
        :param plugin_manager: obj: PluginManager instance
        :param logger: obj: logger for use in the code base for debug messages
        :param arguments: list: command args specific to the command
        """
        if device_name is None or len(device_name) == 0:
            raise RuntimeError('The "device_name" argument cannot be missing '
                               'or "None" or an empty string!')
        self.device_name = device_name
        if configuration is None:
            raise RuntimeError('The "configuration" argument cannot be missing or "None"!')
        self.configuration = configuration
        if plugin_manager is None or not isinstance(plugin_manager, PluginManager):
            raise RuntimeError('The "plugin_manager" argument cannot be missing, "None" or a different type!')
        self.plugin_manager = plugin_manager
        self.logger = logger

        additional_arguments["device_name"] = self.device_name,
        additional_arguments["configuration"] = self.configuration,
        additional_arguments["plugin_manager"] = self.plugin_manager,
        additional_arguments["logger"] = self.logger,
        self.additional_arguments = additional_arguments
        self.command_args = additional_arguments

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

    def __eq__(self, other):
        if isinstance(other, CommandResult):
            if (self.return_code == other.return_code and
                    self.message == other.message and
                    self.device_name == other.device_name):
                return True
        return False
