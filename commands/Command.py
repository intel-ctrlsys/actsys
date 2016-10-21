"""
Defines the layout of a command object
"""
from abc import ABCMeta, abstractmethod


class Command(object):
    """
    Abstract Base Class for all command objects. Ensure derived objects follow its conventions.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, node_name, args=None):
        pass

    @abstractmethod
    def execute(self):
        """How the command is performed"""
        pass


class CommandResult(object):
    """How the result of commands is stored"""

    def __init__(self, return_code=-1, message="Unknown"):
        """Retrieve dependecies and prepare for power on"""
        self.return_code = return_code
        self.message = message

    def __str__(self):
        return "{} - {}".format(self.return_code, self.message)
