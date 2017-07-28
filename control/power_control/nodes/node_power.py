# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements a power_control plugin for controlling nodes.
"""
from __future__ import print_function
import time
import os
from control.utilities.remote_access_data import RemoteAccessData
from control.utilities.utilities import Utilities
from ...plugin import DeclarePlugin
from ..power_control import PowerControl


@DeclarePlugin('node_power', 100)
class NodePower(PowerControl):
    """This class controls node power using a PDU, BMC, and the node OS.
            OPTIONS CONTRACT FOR CONSTRUCTOR
        ---------------------------------
        options = {
            'plugin_manager': self.manager,
            'device_list': [{
                'device_id': 'test_node',
                'hostname': 'test_node',
                'device_type': 'node',
                'access_type': 'mock',
                'bmc': 'test_bmc',
                'pdu_list': [
                    (self.switch_access1, self.switch_plugin1, '3'),
                    (self.switch_access2, self.switch_plugin2, '1')
                ],
                "ip_address": "127.0.0.1",
                "port": 21,
                "user": username,
                "password": password,
                'os_shutdown_timeout_seconds': .2,
                'os_boot_timeout_seconds': .2,
                'os_network_to_halt_time': .2,
                'bmc_boot_timeout_seconds': .2,
                'bmc_chassis_off_wait': .1
            }],
            'bmc_list': [{
                'device_name': 'test_node',
                'hostname': 'test_bmc',
                'device_type': 'bmc',
                'access_type': 'mock',
                "ip_address": "127.0.0.2",
                "port": 21,
                "user": username,
                "password": password
                }]
        }

    """
    def __init__(self, **kwargs):
        """Will throw is bad or missing data is passed in options."""
        PowerControl.__init__(self, kwargs)
        self.__args = kwargs
        if self.__args is None or self.__args == dict():
            raise RuntimeError('The options parameter to this class must not '
                               'be None!')
        self.target_state = None
        self.result_dict = {}
        self.force_on_failure = False
        self.os_access = None
        self.os_credentials = None
        self.force_on_failure = None
        self.target_state = None
        self.policy = None
        self.bmc_credentials = None
        self.bmc_access = None
        self.switches = None
        self.device_name = None
        self.device_type = None
        self.utils = Utilities()

    def get_current_device_power_state(self):
        """
        Get the current device power state. Returns list of 'On', 'Off',
        'On:bmc_on'

        Will raise RuntimeError if wrong device type or the hard switches are
        off.
        """
        device_list = self.__args['device_list']
        bmc_list = self.__args['bmc_list']
        de_duplicated_bmc_list = self.utils.remove_duplicates_from_bmc_data(bmc_list)
        self.utils.map_devices_to_bmc(device_list, de_duplicated_bmc_list,
                                      self._get_power_devices_connected_bmc)
        return self.result_dict

    def _get_power_devices_connected_bmc(self, device_list, bmc):
        for node in device_list:
            hostname = node['hostname']
            try:
                options = self._options_from_node(node, bmc)
                self._parse_options(options)
                self.result_dict[hostname] = self._get_power_state_from_bmc()
            except RuntimeError as run_err:
                self.result_dict[hostname] = run_err.message

    def _get_power_state_from_bmc(self):
        self._if_switches_off_exception()
        if self.bmc_access.get_chassis_state(self.bmc_credentials):
            result = 'On'
            if self.os_access.test_connection(self.os_credentials):
                result += ':bmc_on'
            return result
        else:
            return 'Off'

    def set_device_power_state(self, target_state, force_on_failure=False):
        """
        Set the current power target.  One of 'On', 'Off', 'On:<bmc_state>'
        """
        self.target_state = target_state
        self.force_on_failure = force_on_failure
        device_list = self.__args['device_list']
        bmc_list = self.__args['bmc_list']
        de_duplicated_bmc_list = self.utils.remove_duplicates_from_bmc_data(bmc_list)
        self.utils.map_devices_to_bmc(device_list, de_duplicated_bmc_list,
                                      self._set_power_devices_connected_bmc)
        return self.result_dict

    def _set_power_devices_connected_bmc(self, device_list, bmc):
        for node in device_list:
            hostname = node['hostname']
            try:
                options = self._options_from_node(node, bmc)
                self._parse_options(options)
                self.result_dict[hostname] = self._set_power_state_from_bmc()
            except RuntimeError as run_err:
                self.result_dict[hostname] = run_err.message

    def _set_power_state_from_bmc(self):
        self._if_switches_off_exception()
        if self.target_state == 'Off':
            return self._target_node_off(self.force_on_failure)
        else:
            cmd_pair = self.target_state.split(':')
            if len(cmd_pair) == 1:
                cmd = 'on'
                if self.bmc_access.get_chassis_state(self.bmc_credentials):
                    cmd = 'cycle'
                return self._target_on_to_state(cmd, self.force_on_failure)
            else:
                if cmd_pair[1] == 'bmc_on':
                    return self._target_on_to_state('on',
                                                    self.force_on_failure)
                else:
                    return self._target_on_to_state(cmd_pair[1],
                                                    self.force_on_failure)

    def _report_error(self, message):
        """Report a non-program failure to the appropriate object."""
        str_fmt = "Error: power_control.nodes.node_power.NodePower: {}: {}"
        print(str_fmt.format(self.device_name, message))

    def _parse_options(self, options):
        """Parse the options data contract."""
        self.device_name = options.get('device_name', None)
        if self.device_name is None:
            raise RuntimeError('The device_name passed was None!')
        self.device_type = options.get('device_type', None)
        if self.device_type not in ['node', 'compute', 'service']:
            raise(RuntimeError('NodePower controller used on a non-node type '
                               'device!'))
        self.os_credentials, self.os_access = options['os']

        self.bmc_credentials, self.bmc_access = options['bmc']

        self.switches = options['switches']

        self.policy = options.get('policy', None)
        if not self.policy['OSShutdownTimeoutSeconds']:
            self.policy['OSShutdownTimeoutSeconds'] = 150
        if not self.policy['OSBootTimeoutSeconds']:
            self.policy['OSBootTimeoutSeconds'] = 300
        if not self.policy['OSNetworkToHaltTime']:
            self.policy['OSNetworkToHaltTime'] = 5
        if not self.policy['BMCBootTimeoutSeconds']:
            self.policy['BMCBootTimeoutSeconds'] = 10
        if not self.policy['BMCChassisOffWait']:
            self.policy['BMCChassisOffWait'] = 3

    def _if_switches_off_exception(self):
        """Throw exception if the hard switches are off."""
        result = True
        for switch in self.switches:
            result = result and switch[1].get_switch_state(switch[0], switch[2])
        if not result:
            raise RuntimeError('The prerequisites of the hard switch(es) being '
                               'on was not met!')

    def _target_node_off(self, force):
        """Turn off the node."""
        current_node = self._get_power_state_from_bmc()
        if current_node == 'Off':
            return True
        if current_node == 'On:bmc_on':
            if not self._graceful_os_halt():
                self._report_error("Failed to shutdown node's OS")
                if not force:
                    return False
        result = self.bmc_access.set_chassis_state(self.bmc_credentials, 'off')
        if result:
            name = 'BMCChassisOffWait'
            return self._wait_for_chassis_state(False, self.policy[name])
        else:
            return False

    def _wait_for_chassis_state(self, state, timeout):
        """Wait for the chassis to be in the specified state."""
        start = time.time()
        elapsed = 0
        chassis_state = self.bmc_access.get_chassis_state(self.bmc_credentials)
        while chassis_state is not state and elapsed < timeout:
            chassis_state = self.bmc_access.get_chassis_state(
                self.bmc_credentials)
            time.sleep(1)
            now = time.time()
            elapsed = now - start
        result = elapsed < timeout
        return result

    def _wait_for_network_availability(self, target, timeout):
        """Wait for OS shutdown."""
        start = time.time()
        elapsed = 0
        while self.os_access.test_connection(self.os_credentials) is not target and \
                elapsed < timeout:
            time.sleep(4)
            now = time.time()
            elapsed = now - start
        result = elapsed < timeout
        return result

    def _graceful_os_halt(self):
        """Halt the OS to chassis on not OS."""
        shutdown = os.path.join(os.path.sep, 'sbin', 'shutdown')
        result = self.os_access.execute([shutdown, '--halt', 'now'],
                                        self.os_credentials).return_code
        if result != 255 and result != 0:  # 255 if ssh was disconnected
            self._report_error("Failed to shutdown node's OS")
            return False
        timeout = self.policy['OSShutdownTimeoutSeconds']
        result = self._wait_for_network_availability(False, timeout)
        if result:
            time.sleep(self.policy['OSNetworkToHaltTime'])
        return result

    def _target_on_to_state(self, state, force):
        """Attempt to boot the node to a OS."""
        current = self._get_power_state_from_bmc()
        if current == 'On:bmc_on':
            if not self._graceful_os_halt():
                if not force:
                    return False
            current = self._get_power_state_from_bmc()
        if current == 'Off':
            return self._do_bmc_power_on(state)
        else:
            new_state = state
            if state == "on":
                new_state = "cycle"
            return self._do_simple_bmc_reboot(new_state)

    def _do_bmc_power_on(self, state):
        """Bring up new state from chassis off."""
        result = self.bmc_access.set_chassis_state(self.bmc_credentials, 'on')
        if result:
            if state != 'on':
                result = self.bmc_access.set_chassis_state(self.bmc_credentials,
                                                           state)
            else:
                timeout = self.policy['OSBootTimeoutSeconds']
                result = \
                    self._wait_for_network_availability(True, timeout)
        return result

    def _do_simple_bmc_reboot(self, state):
        """From a non-OS chassis on state reboot to new state."""
        result = self.bmc_access.set_chassis_state(self.bmc_credentials, state)
        if result and state in ['on', 'cycle']:
            timeout = self.policy['OSBootTimeoutSeconds']
            result = \
                self._wait_for_network_availability(True, timeout)
        return result

    def _options_from_node(self, node, bmc):
        """Return the node power control options """

        options = dict()

        try:
            options['device_name'] = node.get("device_id")
            options['device_type'] = node.get("device_type")
            mgr = self.__args['plugin_manager']

            bmc_plugin = mgr.create_instance('bmc', bmc.get("access_type"))
            bmc_credentials = RemoteAccessData(bmc.get("ip_address"), bmc.get("port"),
                                               bmc.get("user"), bmc.get("password"))
            options['bmc'] = (bmc_credentials, bmc_plugin)

            os_plugin = mgr.create_instance('os_remote_access', node.get("access_type"))
            os_access = RemoteAccessData(node.get("ip_address"), node.get("port"),
                                         node.get("user"), node.get("password"))
            options['os'] = (os_access, os_plugin)
        except KeyError as key_error:
            raise RuntimeError("Unable to load access plugin, {}".format(key_error.message))

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
        return options
