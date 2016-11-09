# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Node Power On Procedure plugin.
"""
from ctrl.commands.power_common.power_common import CommonPowerCommand, \
    CommandResult
from ctrl.plugin.manager import PluginMetadataInterface


class PluginMetadata(PluginMetadataInterface):
    """Metadata for this plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'command'

    def name(self):
        """Get the plugin instance name."""
        return 'power_on'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return PowerOnCommand(options)


class PowerOnCommand(CommonPowerCommand):
    """PowerOn command"""
    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(PowerOnCommand, self).__init__(args)

    def _execute_for_node(self):
        """
        Power Node On Procedure:
            1. create proper interface plugin instances here!
            2. build configuration object for NodePower!
            3. if PDUs are off, return failure.
            4. create NodePower plugin instance
            5. if node equals any 'On' state return failure
            6. if any other state, use the NodePower instance to change state
            7. if successful, inform resource manager here
        """
        try:
            # STEP 3
            if not self._test_switch_on_state():
                raise RuntimeError('Hard switches for device {} are off'.
                                   format(self.node_options['device_name']))

            # STEP 4
            if self.power_plugin is None:
                self.power_plugin = self.plugin_manager.\
                    factory_create_instance('power_control', self.plugin_name,
                                            self.node_options)

            # STEP 5
            target, force = self._parse_power_arguments('On:bmc_on', {
                '': 'On:bmc_on',
                'on': 'On:bmc_on',
                'bios': 'On:bios',
                'efi': 'On:efi',
                'hdd': 'On:hdd',
                'pxe': 'On:pxe',
                'removable': 'On:removable',
                'cdrom': 'On:cdrom'
            })
            if target is None:
                raise RuntimeError('Incorrect arguments passed to '
                                   'turn on a node: {}'.
                                   format(self.device_name))

            state = self.power_plugin.get_current_device_power_state()
            if state.startswith('On'):
                raise RuntimeError('Power already on for {}; use '
                                   'power reboot'.
                                   format(self.device_name))

            # STEP 6
            if not self.power_plugin.set_device_power_state(target, force):
                raise RuntimeError('Failed to change state to {} on '
                                   'device {}'.
                                   format(target, self.device_name))

            # STEP 7
            if not self._update_resource_state(True):  # On state
                raise RuntimeError('Failed to inform the resource '
                                   'manager of the state change for '
                                   'device {}'.
                                   format(self.device_name))
        except RuntimeError as err:
            return CommandResult(message=err.message)

        return CommandResult(0, 'Success: Device Powered On: {}'.
                             format(self.device_name))