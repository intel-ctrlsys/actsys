# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Node Power On Procedure plugin.
"""
import time
from .. import CommandResult
from . import CommonPowerCommand
from ...plugin import DeclarePlugin


@DeclarePlugin('power_on', 100)
class PowerOnCommand(CommonPowerCommand):
    """PowerOn command"""
    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 subcommand=None, outlet=None, force=None):
        """Retrieve dependencies and prepare for power on"""
        CommonPowerCommand.__init__(self, device_name, configuration, plugin_manager, logger,
                                    subcommand=subcommand, outlet=outlet, force=force)

    def _execute_for_node(self):
        """
        Power Node On Procedure:
            1. create proper interface plugin instances here!
            2. build configuration object for NodePower!
            3. if PDUs are off, return failure. {Not implemented}
            4. create NodePower plugin instance
            5. if node equals any 'On' state return failure
            6. if any other state, use the NodePower instance to change state
            7. if successful, inform resource manager here
        """
        try:

            # STEP 4
            if self.power_plugin is None:
                self.power_plugin = self.plugin_manager.\
                    create_instance('power_control', self.plugin_name, **self.node_options)

            # STEP 5
            target, force = self._parse_power_arguments('On:bmc_on', {
                '': 'On:bmc_on',
                'on': 'On',
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

            result = []

            power_dict = self.power_plugin.get_current_device_power_state()
            for key, value in power_dict.items():
                if value.startswith('On'):
                    command_result = CommandResult(-1, 'Power on for {}; Device is already Powered on'.format(key))
                    command_result.device_name = key
                    self.device_name.remove(key)
                    result.append(command_result)
            if not self.device_name:
                return result
            else:
                self.node_options, plugin_name = self._options_from_node()

            # STEP 6
            power_dict = self.power_plugin.set_device_power_state(target, force)

            for key, value in power_dict.items():
                if value and isinstance(value, bool):
                    command_result = CommandResult(0, 'Success: Device Powered On: {}'.format(key))
                    command_result.device_name = key
                    result.append(command_result)
                else:
                    command_result = CommandResult(-1, 'Failed to change state to On on device {}: {}'.format(key,
                                                                                                              value))
                    command_result.device_name = key
                    result.append(command_result)

            # If a wait time is set, wait
            device = self.configuration.get_node(self.device_name[0])
            if getattr(device, 'wait_time_after_boot_services', None) and \
                    getattr(device, 'service_list', None):
                # We must wait here to allow systemctl time to enable services.
                self.logger.debug("Waiting for {} seconds for systemctl services to "
                                  "enable...".format(device.wait_time_after_boot_services))
                time.sleep(device.wait_time_after_boot_services)

            # Start the service for the node
            service_result_list = self._update_services("start")

            for item in service_result_list:
                result.append(item)

            # Add node to the resource pool
            if not self._update_resource_state("add"):  # On state
                raise RuntimeError('Failed to inform the resource manager of the state change for '
                                   'device {}'.format(self.device_name))

        except RuntimeError as err:
            return [CommandResult(message=str(err))]

        return result

    def _execute_for_power_switches(self):
        """"""
        return self.switch_pdu("on")
