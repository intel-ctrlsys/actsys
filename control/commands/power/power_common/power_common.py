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
        node = cfg.get_device(self.device_name)

        if not node:
            raise RuntimeError("Device {} was not found in the "
                               "configuration".format(self.device_name))
        options = dict()
        options['device_name'] = node.device_id
        options['device_type'] = node.device_type
        # BMC
        if node and hasattr(node, "bmc") and node.bmc is not None:
            # TODO: check if bmc access_type is not defined.
            bmc_plugin = mgr.factory_create_instance('bmc', node.bmc.access_type)
            bmc_access = RemoteAccessData(node.bmc.ip_address, node.bmc.port,
                                          node.bmc.user, node.bmc.password)
            options['bmc'] = (bmc_access, bmc_plugin)
        # Device OS
        if node:
            # TODO: Check if node access type is not defined
            try:
                os_plugin = self.plugin_manager.factory_create_instance('os_remote_'
                                                                        'access',
                                                                        node.access_type)
                os_access = RemoteAccessData(node.ip_address, node.port,
                                             node.user, node.password)
                options['os'] = (os_access, os_plugin)
            except KeyError as ke:
                self.logger.warning("Unable to load access plugin, {}".format(ke.message))

            # TODO: Check if all of these exist, is there a default?!?!?
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
        """Inform the resource manager that the node can be added or removed."""
        if new_state not in ['add', 'remove']:
            return False

        self.logger.debug("Removing {} from the resource pool.".format(self.device_name))
        resource_pool = self.plugin_manager.factory_create_instance('command',
                                                                    'resource_pool_{}'.format(new_state),
                                                                    self.command_args)
        resource_pool_command_result = resource_pool.execute()
        if resource_pool_command_result.return_code != 0:
            err_msg = "Power command failed due to failed resource {}.".format(new_state)
            self.logger.fatal(err_msg)
            return False

        return True

    def _update_services(self, new_state):
        """Inform the node systemctl that the services can be started or stopped."""
        if new_state not in ['start', 'stop']:
            return False

        self.logger.debug("{}ing services for {}".format(new_state, self.device_name))
        service_stop = self.plugin_manager.factory_create_instance('command', 'service_{}'.format(new_state),
                                                                   self.command_args)
        service_stop_result = service_stop.execute()
        if service_stop_result.return_code != 0:
            err_msg = "Failed power command due to failed service {}.".format(new_state)
            self.logger.fatal(err_msg)
            return False

        return True

    def _parse_power_arguments(self, default_target, targets):
        target = default_target
        if self.args is not None:
            force = self.args.force
            if self.args.subcommand is not None:
                try:
                    target = targets[self.args.subcommand]
                except KeyError:
                    target = None
            return target, force
        else:
            return None, None

    def _execute_for_node(self):
        return CommandResult(message='"CommonPowerCommand._execute_for_node" '
                                     'Not Implemented')

    def _execute_for_power_switches(self):
        return CommandResult(message='"CommonPowerCommand._execute_for_power'
                                     '_switches" Not Implemented')

    def switch_pdu(self, new_state):
        device = self.configuration.get_pdu(self.device_name)

        if device is None or device.device_type != "pdu":
            return CommandResult(1, 'Invalid device type: Cannot toggle device type {}'.format(device.device_type))

        pdu = self.plugin_manager.factory_create_instance('pdu', device.access_type)
        remote_access = RemoteAccessData(str(device.ip_address), device.port, str(device.user), str(device.password))
        outlet_state = pdu.get_outlet_state(remote_access, str(self.args.outlet))
        self.logger.info("{} outlet is currently set to state: {}".format(self.device_name, outlet_state))
        if outlet_state == new_state:
            return CommandResult(0, '{} was already {}, no change made.'.format(self.device_name, new_state))
        try:
            pdu.set_outlet_state(remote_access, str(self.args.outlet), new_state)
            self.logger.info("{} outlet is currently set to state: {}".format(self.device_name, new_state))
        except RuntimeError as ex:
            return CommandResult(1, ex.message)
        return CommandResult(0, 'Successfully switched {} {}'.format(self.device_name, new_state))