# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Common functionality between power commands.
"""
from control.commands import Command, CommandResult
from control.utilities.remote_access_data import RemoteAccessData


class CommonPowerCommand(Command):
    """Common functionality"""

    def __init__(self, args=None):
        Command.__init__(self, args)
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
        return dispatch[self.configuration.get_device(self.device_name).get("device_type")]()

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
        options['device_name'] = node.get("device_id")
        options['device_type'] = node.get("device_type")
        options['bmc_fa_port'] = node.get("bmc_fa_port", None)
        # BMC
        if node and node.get("bmc"):
            bmc = cfg.get_device(node.get("bmc"))
            if bmc is not None:
                # TODO: check if bmc access_type is not defined.
                bmc_plugin = mgr.create_instance('bmc', bmc.get("access_type"))
                bmc_access = RemoteAccessData(bmc.get("ip_address"), bmc.get("port"),
                                              bmc.get("user"), bmc.get("password"))
                options['rest_server_port'] = bmc.get("rest_server_port", None)
                options['bmc'] = (bmc_access, bmc_plugin)

        # Device OS
        if node:
            # TODO: Check if node access type is not defined
            try:
                os_plugin = self.plugin_manager.create_instance('os_remote_access', node.get("access_type"))
                os_access = RemoteAccessData(node.get("ip_address"), node.get("port"),
                                             node.get("user"), node.get("password"))
                options['os'] = (os_access, os_plugin)
            except KeyError as ke:
                self.logger.warning("Unable to load access plugin, {}".format(ke.message))

            # TODO: Check if all of these exist, is there a default?!?!?
            options['policy'] = {
                'OSShutdownTimeoutSeconds': node.get("os_shutdown_timeout_seconds"),
                'OSBootTimeoutSeconds': node.get("os_boot_timeout_seconds"),
                'OSNetworkToHaltTime': node.get("os_network_to_halt_time"),
                'BMCBootTimeoutSeconds': node.get("bmc_boot_timeout_seconds"),
                'BMCChassisOffWait': node.get("bmc_chassis_off_wait")
            }
        options['switches'] = list()
        if node.get("pdu_list", None) is not None:
            options['switches'] = node.get("pdu_list")
        power_plugin_name = node.get("device_power_control", 'node_power')

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
        resource_pool = self.plugin_manager.create_instance('command',
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
        service_stop = self.plugin_manager.create_instance('command', 'service_{}'.format(new_state),
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
        """Execute PDU commands"""
        devices = self.configuration.get_pdu(self.device_name)

        if devices is not None and len(devices) == 1:
            device = devices[0]
            if self.args.outlet is None:
                return CommandResult(1, 'PDU outlet not specified. Please use -o <outlet> to specify outlet\n'
                                        'Usage : $ctrl power {on,off} -o <outlet> <pdu_name>\n')
            pdu = self.plugin_manager.create_instance('pdu', device.get("access_type"))
            remote_access = RemoteAccessData(str(device.get("ip_address")), device.get("port"), str(device.get("user")),
                                             str(device.get("password")))
            try:
                outlet_state = pdu.get_outlet_state(remote_access, str(self.args.outlet))
            except RuntimeError as pdu_ex:
                return CommandResult(1, pdu_ex.message)
            self.logger.info("{} outlet is currently set to state: {}".format(self.device_name, outlet_state))
            if outlet_state.upper() == new_state.upper():
                return CommandResult(0, '{} outlet {} was already {}, no change '
                                        'made.'.format(self.device_name, self.args.outlet, new_state))
            try:
                pdu.set_outlet_state(remote_access, str(self.args.outlet), new_state)
                self.logger.info("{} outlet is currently set to state: {}".format(self.device_name, new_state))
            except RuntimeError as ex:
                return CommandResult(1, ex.message)
        else:
            return CommandResult(1, 'No PDU or more than one PDU was found for the device\n'
                                    'Usage : $ctrl power {on,off} -o <outlet> <pdu_name>\n')
        return CommandResult(0, 'Successfully switched {} {}'.format(self.device_name, new_state))
