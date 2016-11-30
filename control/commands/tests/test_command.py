# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the Command and CommandResult.
"""
import unittest
from .. import Command, CommandResult
from ...plugin.manager import PluginManager


class TestCommandResult(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""

    def setUp(self):
        self.result = 0
        self.message = 'The strangest return message ever.!/@3<>-+='
        self.command_result = CommandResult(self.result, self.message)

    def test_str(self):
        """Stub test, please update me"""

        self.assertEqual(self.command_result.__str__(),
                         '{} - {}'.format(self.result, self.message))


class TestCommand(unittest.TestCase):
    def test(self):
        instance = Command({'device_name': 'node_name',
                            'configuration': [],  # Placeholder
                            'plugin_manager': PluginManager(),
                            'logger': None,
                            'arguments': None})
        instance.execute()
        Command({'device_name': 'node_name',
                 'configuration': [],  # Placeholder
                 'plugin_manager': PluginManager(),
                 'unknown_param': None})
        with self.assertRaises(RuntimeError):
            Command(None)
        with self.assertRaises(RuntimeError):
            Command({'configuration': [],  # Placeholder
                     'plugin_manager': PluginManager()})  # Placeholder
        with self.assertRaises(RuntimeError):
            Command({'device_name': None,
                     'configuration': [],  # Placeholder
                     'plugin_manager': PluginManager()})  # Placeholder
        with self.assertRaises(RuntimeError):
            Command({'device_name': '',
                     'configuration': [],  # Placeholder
                     'plugin_manager': PluginManager()})
        with self.assertRaises(RuntimeError):
            Command({'device_name': 'node_name',
                     'plugin_manager': PluginManager()})
        with self.assertRaises(RuntimeError):
            Command({'device_name': 'node_name',
                     'configuration': None,
                     'plugin_manager': PluginManager()})
        with self.assertRaises(RuntimeError):
            Command({'device_name': 'node_name',
                     'configuration': [],  # Placeholder
                     'plugin_manager': None})  # Placeholder
        with self.assertRaises(RuntimeError):
            Command({'device_name': 'node_name',
                     'configuration': []})  # Placeholder
        with self.assertRaises(RuntimeError):
            Command({'device_name': 'node_name',
                     'configuration': [],  # Placeholder
                     'plugin_manager': self})

    def test_get_name(self):
        command = Command({'device_name': 'node_name',
                            'configuration': [],  # Placeholder
                            'plugin_manager': PluginManager(),
                            'logger': None,
                            'arguments': None})
        self.assertEqual(command.get_name(), "Command")


if __name__ == '__main__':
    unittest.main()
