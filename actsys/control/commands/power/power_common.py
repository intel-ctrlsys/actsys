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

    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 subcommand=None, outlet=None, force=None):
        Command.__init__(self, device_name, configuration, plugin_manager, logger,
                         subcommand=subcommand, outlet=outlet, force=force)
        self.subcommand = subcommand
        self.outlet = outlet
        self.force = force
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
        return dispatch[self.configuration.get_device(self.device_name[0]).get("device_type")]()

    def _options_from_node(self):
        """Return the node power control options based on the node_name and
                   configuration object."""
        device_list = []
        bmc_list = []
        options = {}
        node = None
        power_plugin_name = None
        for device in self.device_name:
            node = self.configuration.get_device(device)
            device_list.append(node)
            bmc_list.append(self.configuration.get_device(node.get("bmc")))
        if node:
            power_plugin_name = node.get("device_power_control", 'node_power')
        options['device_list'] = device_list
        options['bmc_list'] = bmc_list
        options['plugin_manager'] = self.plugin_manager
        return options, power_plugin_name

    def _update_resource_state(self, new_state):
        """Inform the resource manager that the node can be added or removed."""
        self.logger.debug("{}ing {} from the resource pool.".format(new_state, self.device_name))
        resource_pool = self.plugin_manager.create_instance('command', 'resource_pool_{}'.format(new_state),
                                                            device_name=self.device_name,
                                                            configuration=self.configuration,
                                                            plugin_manager=self.plugin_manager, logger=self.logger)
        resource_pool_command_result = resource_pool.execute()
        if resource_pool_command_result.return_code != 0:
            err_msg = "Power command failed due to failed resource {}.".format(new_state)
            self.logger.critical(err_msg)
            return False

        return True

    def _update_services(self, new_state):
        """Inform the node systemctl that the services can be started or stopped."""
        self.logger.debug("{}ing services for {}".format(new_state, self.device_name))
        service_stop = self.plugin_manager.create_instance('command', 'service_{}'.format(new_state),
                                                           device_name=self.device_name,
                                                           configuration=self.configuration,
                                                           plugin_manager=self.plugin_manager, logger=self.logger)
        service_stop_result = service_stop.execute()
        return service_stop_result

    def _parse_power_arguments(self, default_target, targets):
        target = default_target
        force = self.force
        if self.subcommand is not None:
            try:
                target = targets[self.subcommand]
            except KeyError:
                target = None
        return target, force

    @classmethod
    def _execute_for_node(cls):
        return CommandResult(message='"CommonPowerCommand._execute_for_node" '
                                     'Not Implemented')

    @classmethod
    def _execute_for_power_switches(cls):
        return CommandResult(message='"CommonPowerCommand._execute_for_power'
                                     '_switches" Not Implemented')

    def switch_pdu(self, new_state):
        """Execute PDU commands"""
        result = []

        for device in self.device_name:
            devices = self.configuration.get_pdu(device)

            if devices is not None and len(devices) == 1:
                device = devices[0]
                if self.outlet is None:
                    result.append(CommandResult(1, 'PDU outlet not specified. Please use -o <outlet> to specify'
                                                ' outlet\n Usage : $ctrl power {on,off} -o <outlet>'
                                                ' <pdu_name>\n'))
                    continue
                pdu = self.plugin_manager.create_instance('pdu', device.get("access_type"))
                remote_access = RemoteAccessData(str(device.get("ip_address")), device.get("port"),
                                                 str(device.get("user")),
                                                 str(device.get("password")))
                try:
                    outlet_state = pdu.get_outlet_state(remote_access, str(self.outlet))
                except RuntimeError as pdu_ex:
                    result.append(CommandResult(1, str(pdu_ex)))
                    continue
                self.logger.info("{} outlet is currently set to state: {}".format(device, outlet_state))
                if outlet_state.upper() == new_state.upper():
                    result.append(CommandResult(0, '{} outlet {} was already {}, no change '
                                                'made.'.format(device, self.outlet, new_state)))
                    continue
                try:
                    pdu.set_outlet_state(remote_access, str(self.outlet), new_state)
                    self.logger.info("{} outlet is currently set to state: {}".format(device, new_state))
                except RuntimeError as ex:
                    result.append(CommandResult(1, str(ex)))
                    continue
            else:
                result.append(CommandResult(1, 'No PDU or more than one PDU was found for the device\n '
                                            'Usage : $ctrl power {on,off} -o <outlet> <pdu_name>\n'))
                continue
            result.append(CommandResult(0, 'Successfully switched {} {}'.format(device, new_state)))

        return result
