# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Common functionality between power commands.
"""
from ctrl.commands import Command, CommandResult
from ctrl.utilities.remote_access_data import RemoteAccessData


class CommonPowerCommand(Command):
    """Common functionality"""
    def __init__(self, args=None):
        super(CommonPowerCommand, self).__init__(args)
        self.power_plugin = None

        # Step 1 & 2
        self.node_options, self.plugin_name = self._options_from_node()

    def execute(self):
        """Dispatch based on device type"""
        dispatch = {
            'node': self._execute_for_node,
            'compute': self._execute_for_node,
            'service': self._execute_for_node,
            'master': self._execute_for_node,
            'login': self._execute_for_node,
            'pdu': self._execute_for_power_switches,
            'power_switch': self._execute_for_power_switches
        }
        # dispatch[self.configuration.get_device_param('type')]()
        return dispatch['node']()  # TODO: from configuration

    def _options_from_node(self):
        """Return the node power control options based on the node_name and
           configuration object."""
        # TODO These should come from the configuration.
        bmc_plugin = self.plugin_manager.factory_create_instance('bmc')
        bmc_access = RemoteAccessData('192.168.255.2', 623, 'root', 'pdamons')
        os_plugin = self.plugin_manager.factory_create_instance('os_remote_'
                                                                'access')
        os_access = RemoteAccessData('192.168.255.1', 22, 'pdamons', None)

        options = {
            'device_name': self.device_name,
            'device_type': 'node',
            'os': (os_access, os_plugin),
            'bmc': (bmc_access, bmc_plugin),
            'switches': [],  # TODO: for testing only, replace.
            'policy': {
                'OSShutdownTimeoutSeconds': 150,
                'OSBootTimeoutSeconds': 300,
                'OSNetworkToHaltTime': 5,
                'BMCBootTimeoutSeconds': 10,
                'BMCChassisOffWait': 3
            }
        }
        return options, 'node_power'  # TODO: name from config...

    def _test_switch_on_state(self):
        """If hard switches are off turn on or return False."""
        if len(self.node_options['switches']) == 0:
            return True
        else:
            return False  # TODO: Implement this step here!

    def _update_resource_state(self, new_state):
        """Inform the resource manager that the node is now on-line."""
        valid_node_types = {'node', 'compute', 'service', 'master', 'login'}
        # TODO: Implement this step here!
        device_type = 'node'  # From self.configuration in the future...
        return device_type in valid_node_types

    def _parse_power_arguments(self, default_target, targets):
        force = False
        target = default_target
        if self.command_args is not None:
            for arg in self.command_args:
                if arg == 'force':
                    force = True
                elif arg in targets:
                    target = targets[arg]
                else:
                    return None, None
            return target, force
        else:
            return None, None

    def _execute_for_node(self):
        return CommandResult(message='"CommonPowerCommand._execute_for_node" '
                                     'Not Implemented')

    def _execute_for_power_switches(self):
        return CommandResult(message='"CommonPowerCommand._execute_for_power'
                                     '_switches" Not Implemented')
