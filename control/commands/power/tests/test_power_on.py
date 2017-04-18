# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the PowerOnCommand.
"""
from .. import PowerOnCommand
from .power_fixures import *


class MockStepUpdateResource(PowerOnCommand):
    """Fail resource update mocked object"""
    def __init__(self, **options):
        super(MockStepUpdateResource, self).__init__(**options)

    def _update_resource_state(self, new_state):
        return False


class TestPowerOnCommand(PowerCommandsCommon):
    """Test case for the PowerOnNodeCommand class."""
    def setUp(self):
        super(TestPowerOnCommand, self).setUp()
        self.write_state('Off')
        self.command_options["subcommand"] = 'on'
        self.command = PowerOnCommand(**self.command_options)
        self.command.plugin_name = 'mock'

    def test_positive_on_from_off(self):
        result = self.command.execute()
        self.assertEqual('Success: Device Powered On: test_node',
                         result.message)
        self.assertEqual(0, result.return_code)

    def test_step_3_exception(self):
        self.command.node_options['switches'] = {
            (object(), object(), object()),
            (object(), object(), object())
        }
        result = self.command.execute()
        self.assertEqual('Hard switches for device test_node are off',
                         result.message)
        self.assertEqual(-1, result.return_code)

    def test_power_plugin_object_exists(self):
        self.command.power_plugin = self.manager.\
            create_instance('power_control', 'mock', **self.command.node_options)
        result = self.command.execute()
        self.assertEqual('Success: Device Powered On: test_node',
                         result.message)
        self.assertEqual(0, result.return_code)

    def test_parse_arguments(self):
        self.command.force = None
        self.command.subcommand = 'bad_subcommand'
        result = self.command.execute()
        self.assertEqual('Incorrect arguments passed to turn on a node: '
                         'test_node', result.message)
        self.assertEqual(-1, result.return_code)

    def test_parse_arguments_2(self):
        self.args = None
        result = self.command.execute()
        self.assertEqual('Success: Device Powered On: test_node',
                         result.message)
        self.assertEqual(0, result.return_code)

    def test_parse_arguments_3(self):
        self.command.subcommand = 'unknown'
        result = self.command.execute()
        self.assertEqual('Incorrect arguments passed to turn on a node: '
                         'test_node', result.message)
        self.assertEqual(-1, result.return_code)

    def test_parse_arguments_4(self):
        self.command.force = True
        result = self.command.execute()
        self.assertEqual('Success: Device Powered On: test_node',
                         result.message)
        self.assertEqual(0, result.return_code)

    def test_positive_on_from_on(self):
        self.write_state('On:bmc_on')
        result = self.command.execute()
        self.assertEqual('Power already on for test_node; use power cycle',
                         result.message)
        self.assertEqual(-1, result.return_code)

    def test_failure_to_change_state(self):
        self.command.power_plugin = MockPowerPlugin(**self.options)
        result = self.command.execute()
        self.assertEqual('Failed to change state to On:bmc_on on device '
                         'test_node', result.message)
        self.assertEqual(-1, result.return_code)

    def test_failure_to_change_state_with_exception(self):
        self.command.power_plugin = MockPowerPluginException(**self.options)
        result = self.command.execute()
        self.assertEqual('Mock exception', result.message)
        self.assertEqual(-1, result.return_code)

    def test_resource_failure(self):
        cmd = MockStepUpdateResource(**self.command_options)
        cmd.plugin_name = 'mock'
        result = cmd.execute()
        self.assertEqual('Failed to inform the resource manager of the state '
                         'change for device test_node', result.message)
        self.assertEqual(-1, result.return_code)


if __name__ == '__main__':
    unittest.main()
