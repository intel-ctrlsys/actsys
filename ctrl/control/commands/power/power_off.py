#
# Copyright (c) 2016 Intel Corp.
#
"""
Node Power Off Procedure Plugin.
"""
from .. import CommandResult
from . import CommonPowerCommand
from ...plugin import DeclarePlugin


@DeclarePlugin('power_off', 100)
class PowerOffCommand(CommonPowerCommand):
    """PowerOff command"""
    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 subcommand=None, outlet=None, force=None):
        """Retrieve dependencies and prepare for power on"""
        CommonPowerCommand.__init__(self, device_name, configuration, plugin_manager, logger,
                                    subcommand=subcommand, outlet=outlet, force=force)

    def _execute_for_node(self):
        """
        Power Off Node Procedure:
            1. create proper interface plugin instances here!
            2. build configuration object for NodePower!
            3. create NodePower plugin instance
            4. return success if already in the off state
            5. if any other state, use the NodePower instance to change state
            6. if successful, inform resource manager here
        """
        try:
            # STEP 3
            if self.power_plugin is None:
                self.power_plugin = self.plugin_manager.\
                    create_instance('power_control', self.plugin_name, **self.node_options)

            target, force = self._parse_power_arguments('Off', {'off': 'Off'})
            if target is None:
                raise RuntimeError('Incorrect arguments passed to '
                                   'turn off a node: {}'.
                                   format(self.device_name))
            # STEP 5
            if not self._update_resource_state("remove"):
                raise RuntimeError('Failed to inform the resource manager of the state change for '
                                   'device {}'.format(self.device_name))

            # STEP 6: Stop node service
            if not self._update_services("stop"):  # On state
                raise RuntimeError('Failed to start the services for device {}'.format(self.device_name))

            # STEP 7
            self.logger.debug('Attempting to change state to {} on device {}'.format(target, self.device_name))
            if not self.power_plugin.set_device_power_state(target, force):
                raise RuntimeError('Failed to change state to {} on device {}'.format(target, self.device_name))

        except RuntimeError as err:
            return CommandResult(message=err.message)

        return CommandResult(0, 'Success: Power Off {}'.
                             format(self.device_name))

    def _execute_for_power_switches(self):
        """"""
        return self.switch_pdu("off")