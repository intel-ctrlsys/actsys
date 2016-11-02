#
# Copyright (c) 2016 Intel Corp.
#
"""
Node Power Off Procedure Plugin.
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
        return 'node_power_off'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return PowerOffCommand(options)


class PowerOffCommand(CommonPowerCommand):
    """PowerOff command"""
    def __init__(self, args):
        """Retrieve dependencies and prepare for power on"""
        super(PowerOffCommand, self).__init__(args)

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
                    factory_create_instance('power_control', self.plugin_name,
                                            self.node_options)

            target, force = self._parse_power_arguments('Off', {'off': 'Off'})
            if target is None:
                raise RuntimeError('Incorrect arguments passed to '
                                   'turn off a node: {}'.
                                   format(self.device_name))

            # Step 4
            state = self.power_plugin.get_current_device_power_state()
            if state == 'Off':
                return CommandResult(0, 'Success: Power Off {}'.
                                     format(self.device_name))

            # STEP 5
            if not self.power_plugin.set_device_power_state(target, force):
                raise RuntimeError('Failed to change state to {} on '
                                   'device {}'.
                                   format(target, self.device_name))

            # STEP 6
            if not self._update_resource_state(False):
                raise RuntimeError('Failed to inform the resource '
                                   'manager of the state change for '
                                   'device {}'.
                                   format(self.device_name))
        except RuntimeError as err:
            return CommandResult(message=err.message)

        return CommandResult(0, 'Success: Power Off {}'.
                             format(self.device_name))
