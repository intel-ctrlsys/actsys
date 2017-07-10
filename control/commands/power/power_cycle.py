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

    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 subcommand=None, outlet=None, force=None):
        """Retrieve dependencies and prepare for power reboot"""
        CommonPowerCommand.__init__(self, device_name, configuration, plugin_manager, logger,
                                    subcommand=subcommand, outlet=outlet, force=force)

    def _execute_for_node(self):
        """
        Power Node Cycle Procedure:
            1. create proper interface plugin instances here!
            2. build configuration object for NodePower!
            3. if PDU is off, return an error!!! {Not implemented}
            4. create NodePower plugin instance
            5. if state is off, return an error (use power on).
            6. if any other state, use the NodePower instance to change state
            7. if successful, inform resource manager here
        """
        try:
            # STEP 4
            if self.power_plugin is None:
                self.power_plugin = self.plugin_manager.create_instance('power_control', self.plugin_name,
                                                                        **self.node_options)

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

            result = []

            power_dict = self.power_plugin.get_current_device_power_state()
            for key, value in power_dict.iteritems():
                if value == 'Off':
                    command_result = CommandResult(-1, 'Power off for {}; use the power on command'.format(key))
                    command_result.device_name = key
                    self.device_name.remove(key)
                    result.append(command_result)
            if not self.device_name:
                return result
            else:
                self.node_options, plugin_name = self._options_from_node()

            # STEP 5
            if not self._update_resource_state("remove"):
                raise RuntimeError('Failed to inform the resource manager of the state change for '
                                   'device {}'.format(self.device_name))

            # STEP 6
            power_dict = self.power_plugin.set_device_power_state(target, force)

            # STEP 7
            if not self._update_resource_state("add"):  # On state
                raise RuntimeError('Failed to inform the resource manager of the state change for '
                                   'device {}'.format(self.device_name))

            for key, value in power_dict.iteritems():
                if value and isinstance(value, bool):
                    command_result = CommandResult(0, 'Success: Device Cycled: {}'.format(key))
                    command_result.device_name = key
                    result.append(command_result)
                else:
                    command_result = CommandResult(-1, 'Failed to change state to {} on '
                                                        'device {}'.format(target, key))
                    command_result.device_name = key
                    result.append(command_result)

        except RuntimeError as err:
            return [CommandResult(message=err.message)]

        return result
