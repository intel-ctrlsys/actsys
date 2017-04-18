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
                    create_instance('power_control', self.plugin_name, **self.node_options)

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
                                   'power cycle'.
                                   format(self.device_name))
            # STEP 6
            if not self.power_plugin.set_device_power_state(target, force):
                raise RuntimeError('Failed to change state to {} on '
                                   'device {}'.
                                   format(target, self.device_name))

            # If a wait time is set, wait
            device = self.configuration.get_node(self.device_name)
            if getattr(device, 'wait_time_after_boot_services', None) and \
                    getattr(device, 'service_list', None):
                # We must wait here to allow systemctl time to enable services.
                self.logger.debug("Waiting for {} seconds for systemctl services to "
                                  "enable...".format(device.wait_time_after_boot_services))
                time.sleep(device.wait_time_after_boot_services)

            # Start the service for the node
            if not self._update_services("start"):  # On state
                raise RuntimeError('Failed to start the services for device {}'.format(self.device_name))

            # Add node to the resource pool
            if not self._update_resource_state("add"):  # On state
                raise RuntimeError('Failed to inform the resource manager of the state change for '
                                   'device {}'.format(self.device_name))

        except RuntimeError as err:
            return CommandResult(message=err.message)

        return CommandResult(0, 'Success: Device Powered On: {}'.
                             format(self.device_name))

    def _execute_for_power_switches(self):
        """"""
        return self.switch_pdu("on")
