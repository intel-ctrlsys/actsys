# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Node Power Cycle Procedure plugin.
"""
from .. import CommandResult
from . import CommonPowerCommand
from ...plugin import DeclarePlugin


@DeclarePlugin('power_cycle', 100)
class PowerCycleCommand(CommonPowerCommand):
    """Power reboot command"""

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power reboot"""
        CommonPowerCommand.__init__(self, args)

    def _execute_for_node(self):
        """
        Power Node Cycle Procedure:
            1. create proper interface plugin instances here!
            2. build configuration object for NodePower!
            3. if PDU is off, return an error!!!
            4. create NodePower plugin instance
            5. if state is off, return an error (use power on).
            6. if any other state, use the NodePower instance to change state
            7. if successful, inform resource manager here
        """
        try:
            # STEP 3
            if not self._test_switch_on_state():
                raise RuntimeError('Hard switches for device {} are off'.format(self.node_options['device_name']))

            # STEP 4
            if self.power_plugin is None:
                self.power_plugin = self.plugin_manager.create_instance('power_control', self.plugin_name,
                                                                        self.node_options)

            # STEP 5
            target, force = self._parse_power_arguments('On:bmc_on', {
                '': 'On:bmc_on',
                'cycle': 'On:bmc_on',
                'bios': 'On:bios',
                'efi': 'On:efi',
                'hdd': 'On:hdd',
                'pxe': 'On:pxe',
                'removable': 'On:removable',
                'cdrom': 'On:cdrom'
            })
            if target is None:
                raise RuntimeError('Incorrect arguments passed to cycle a node: {}'.format(self.device_name))

            state = self.power_plugin.get_current_device_power_state()
            if state == 'Off':
                raise RuntimeError('Power off for {}; use the '
                                   'power on command'.
                                   format(self.device_name))

            # STEP 5
            if not self._update_resource_state("remove"):
                raise RuntimeError('Failed to inform the resource manager of the state change for '
                                   'device {}'.format(self.device_name))

            # STEP 6
            if not self.power_plugin.set_device_power_state(target, force):
                raise RuntimeError('Failed to change state to {} on '
                                   'device {}'.
                                   format(target, self.device_name))

            # STEP 7
            if not self._update_resource_state("add"):  # On state
                raise RuntimeError('Failed to inform the resource manager of the state change for '
                                   'device {}'.format(self.device_name))

        except RuntimeError as err:
            return CommandResult(message=err.message)

        return CommandResult(0, 'Success: Device Cycled: {}'.
                             format(self.device_name))
