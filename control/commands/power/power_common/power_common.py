# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Common functionality between power commands.
"""
from ... import Command, CommandResult
from ....utilities.remote_access_data import RemoteAccessData


class CommonPowerCommand(Command):
    """Common functionality"""
    def __init__(self, args=None):
        super(CommonPowerCommand, self).__init__(args)
        self.power_plugin = None

        # Step 1 & 2
        self.node_options, self.plugin_name = self._options_from_node()

    def execute(self):
        """Dispatch based on device type"""
        # TODO: valid types are 'node', 'pdu', 'psu', 'bmc'. Everything else is roles.
        dispatch = {
            'node': self._execute_for_node,
            'pdu': self._execute_for_power_switches,
        }
        return dispatch[self.configuration.get_device(self.device_name).device_type]()

    def _options_from_node(self):
        """Return the node power control options based on the node_name and
                   configuration object."""
        cfg = self.configuration
        mgr = self.plugin_manager
        # Device
        node = cfg.get_node(self.device_name)

        if not node:
            raise RuntimeError("Device {} was not found in the "
                               "configuration".format(self.device_name))
        options = dict()
        options['device_name'] = node.device_id
        options['device_type'] = node.device_type
        # BMC
        if node and hasattr(node, "bmc"):
            # TODO: check if bmc access_type is not defined.
            bmc_plugin = mgr.factory_create_instance('bmc', node.bmc.access_type)
            bmc_access = RemoteAccessData(node.bmc.ip_address, node.bmc.port,
                                          node.bmc.user, node.bmc.password)
            options['bmc'] = (bmc_access, bmc_plugin)
        # Device OS
        if node:
            # TODO: Check if node access type is not defined
            os_plugin = self.plugin_manager.factory_create_instance('os_remote_'
                                                                    'access',
                                                                    node.access_type)
            os_access = RemoteAccessData(node.ip_address, node.port,
                                         node.user, node.password)
            options['os'] = (os_access, os_plugin)
            # TODO: Chek if all of these exist, is there a default?!?!?
            options['policy'] = {
                'OSShutdownTimeoutSeconds': node.os_shutdown_timeout_seconds,
                'OSBootTimeoutSeconds': node.os_boot_timeout_seconds,
                'OSNetworkToHaltTime': node.os_network_to_halt_time,
                'BMCBootTimeoutSeconds': node.bmc_boot_timeout_seconds,
                'BMCChassisOffWait': node.bmc_chassis_off_wait
            }
        options['switches'] = list()
        if node and hasattr(node, "pdu_list"):
            options['switches'] = node.pdu_list
        power_plugin_name = 'node_power'
        if hasattr(node, "device_power_control"):
            power_plugin_name = node.device_power_control

        return options, power_plugin_name

    def _test_switch_on_state(self):
        """If hard switches are off turn on or return False."""
        if self.node_options['switches'] is None or len(self.node_options['switches']) == 0:
            return True
        else:
            # TODO: Implement this step here when PDU code is completed!
            return False

    def _update_resource_state(self, new_state):
        """Inform the resource manager that the node is now on-line."""
        valid_node_types = {'node', 'compute', 'service', 'master', 'login'}
        # TODO: Update node state in Resource Manager when available!
        device_type = self.configuration.get_device(self.device_name).device_type
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
