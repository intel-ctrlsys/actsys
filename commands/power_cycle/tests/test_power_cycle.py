# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the PowerCycleCommand.
"""
from ctrl.commands.tests.power_fixures import *
from ctrl.commands.power_cycle import PowerCycleCommand
from ctrl.commands.power_cycle import PluginMetadata


class MockStepUpdateResource(PowerCycleCommand):
    """Fail resource update mocked object"""
    def __init__(self, args=None):
        super(MockStepUpdateResource, self).__init__(args)

    def _update_resource_state(self, new_state):
        return False


class TestPowerCycleCommand(PowerCommandsCommon):
    """Test case for the RemoteSshPlugin class."""
    def setUp(self):
        super(TestPowerCycleCommand, self).setUp()
        self.write_state('On:bmc_on')
        self.command_options['arguments'] = ['cycle']
        self.command = PowerCycleCommand(self.command_options)
        self.command.plugin_name = 'mock'

    def test_metadata(self):
        metadata = PluginMetadata()
        self.assertEqual('command', metadata.category())
        self.assertEqual('power_cycle', metadata.name())
        self.assertEqual(100, metadata.priority())
        self.assertIsNotNone(metadata.create_instance(self.command_options))

    def test_positive_on_from_on(self):
        result = self.command.execute()
        self.assertEqual('Success: Device Cycled: test_node',
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

    def test_parse_arguments(self):
        self.command.command_args = None
        result = self.command.execute()
        self.assertEqual('Incorrect arguments passed to cycle a node: '
                         'test_node', result.message)
        self.assertEqual(-1, result.return_code)

    def test_parse_arguments_2(self):
        self.command.command_args = []
        result = self.command.execute()
        self.assertEqual('Success: Device Cycled: test_node',
                         result.message)
        self.assertEqual(0, result.return_code)

    def test_parse_arguments_3(self):
        self.command.command_args = ['unknown']
        result = self.command.execute()
        self.assertEqual('Incorrect arguments passed to cycle a node: '
                         'test_node', result.message)
        self.assertEqual(-1, result.return_code)

    def test_parse_arguments_4(self):
        self.command.command_args = ['force']
        result = self.command.execute()
        self.assertEqual('Success: Device Cycled: test_node',
                         result.message)
        self.assertEqual(0, result.return_code)

    def test_positive_initial_off(self):
        self.write_state('Off')
        result = self.command.execute()
        self.assertEqual('Power off for test_node; use the power on command',
                         result.message)
        self.assertEqual(-1, result.return_code)

    def test_failure_to_change_state(self):
        self.command.power_plugin = MockPowerPlugin(self.options)
        result = self.command.execute()
        self.assertEqual('Failed to change state to On:bmc_on on device '
                         'test_node', result.message)
        self.assertEqual(-1, result.return_code)

    def test_failure_to_change_state_with_exception(self):
        self.command.power_plugin = MockPowerPluginException(self.options)
        result = self.command.execute()
        self.assertEqual('Mock exception', result.message)
        self.assertEqual(-1, result.return_code)

    def test_resource_failure(self):
        cmd = MockStepUpdateResource(self.command_options)
        cmd.plugin_name = 'mock'
        result = cmd.execute()
        self.assertEqual('Failed to inform the resource manager of the state '
                         'change for device test_node', result.message)
        self.assertEqual(-1, result.return_code)


if __name__ == '__main__':
    unittest.main()
