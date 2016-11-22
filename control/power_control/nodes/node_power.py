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
from ...plugin.manager import PluginMetadataInterface
from ..power_control import PowerControl
from ...utilities.utilities import Utilities


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'power_control'

    def name(self):
        """Get the plugin instance name."""
        return 'node_power'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return NodePower(options)


class NodePower(PowerControl):
    """This class controls node power using a PDU, BMC, and the node OS.

        OPTIONS CONTRACT FOR CONSTRUCTOR
        ---------------------------------
        options = {
              'device_name': name,
              'device_type': type,
              'os': (remote_access_data, remote_access_plugin),
              'bmc': (remote_access_data, bmc_plugin),
              'switches':
              [ ### index number is PSU index number zero-based ###
                  (remote_access_data, power_switch_plugin, outlet_id),
                  (remote_access_data, power_switch_plugin, outlet_id),
              ],
              'policy': policy_dictionary_for_this_node
          }
    """
    def __init__(self, options):
        """Will throw is bad or missing data is passed in options."""
        super(NodePower, self).__init__(options)
        self.__options = options
        if self.__options is None:
            raise RuntimeError('The options parameter to this class must not '
                               'be None!')
        self.utilities = Utilities()
        self._parse_options()

    def get_current_device_power_state(self):
        """
        Get the current device power state. Returns one of 'On', 'Off',
        'On:bmc_on'

        Will raise RuntimeError if wrong device type or the hard switches are
        off.
        """
        self._if_switches_off_exception()
        if self.bmc_access.get_chassis_state(self.bmc_credentials):
            result = 'On'
            if self.utilities is not None and \
                    self.utilities.ping_check(self.os_credentials.address):
                result += ':bmc_on'
            return result
        else:
            return 'Off'

    def set_device_power_state(self, target_state, force_on_failure=False):
        """
        Set the current power target.  One of 'On', 'Off', 'On:<bmc_state>'
        """
        self._if_switches_off_exception()
        if target_state == 'Off':
            return self._target_node_off(force_on_failure)
        else:
            cmd_pair = target_state.split(':')
            if len(cmd_pair) == 1:
                cmd = 'on'
                if self.bmc_access.get_chassis_state(self.bmc_credentials):
                    cmd = 'cycle'
                return self._target_on_to_state(cmd, force_on_failure)
            else:
                if cmd_pair[1] == 'bmc_on':
                    return self._target_on_to_state('on',
                                                    force_on_failure)
                else:
                    return self._target_on_to_state(cmd_pair[1],
                                                    force_on_failure)

    def _report_error(self, message):
        """Report a non-program failure to the appropriate object."""
        str_fmt = "Error: power_control.nodes.node_power.NodePower: {}: {}"
        print(str_fmt.format(self.device_name, message))

    def _parse_options(self):
        """Parse the options data contract."""
        self.device_name = self.__options['device_name']
        self.device_type = self.__options['device_type']
        if self.device_type not in ['node', 'compute', 'service']:
            raise(RuntimeError('NodePower controller used on a non-node type '
                               'device!'))
        self.os_credentials, self.os_access = self.__options['os']
        if self.os_access is None:
            raise RuntimeError('The OS access object passed was None!')
        if self.os_credentials is None:
            raise RuntimeError('The OS credentials object passed was None!')
        self.bmc_credentials, self.bmc_access = self.__options['bmc']
        if self.bmc_access is None:
            raise RuntimeError('The BMC access object passed was None!')
        if self.bmc_credentials is None:
            raise RuntimeError('The BMC credentials object passed was None!')
        self.switches = self.__options['switches']
        if self.switches is None:
            self.switches = []
        self.policy = self.__options['policy']
        if self.policy is None or len(self.policy) == 0:
            self.policy = {
                'OSShutdownTimeoutSeconds': 150,
                'OSBootTimeoutSeconds': 300,
                'OSNetworkToHaltTime': 5,
                'BMCBootTimeoutSeconds': 10,
                'BMCChassisOffWait': 3
            }

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
        current_node = self.get_current_device_power_state()
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

    def _wait_for_network_availability(self, address, target, timeout):
        """Wait for OS shutdown."""
        start = time.time()
        elapsed = 0
        while self.utilities.ping_check(address) is not target and \
                elapsed < timeout:
            time.sleep(1)
            now = time.time()
            elapsed = now - start
        result = elapsed < timeout
        return result

    def _graceful_os_halt(self):
        """Halt the OS to chassis on not OS."""
        shutdown = os.path.join(os.path.sep, 'sbin', 'shutdown')
        result = self.os_access.execute([shutdown, '--halt', 'now'],
                                        self.os_credentials)[0]
        if result != 255 and result != 0:  # 255 if ssh was disconnected
            self._report_error("Failed to shutdown node's OS")
            return False
        timeout = self.policy['OSShutdownTimeoutSeconds']
        address = self.os_credentials.address
        result = self._wait_for_network_availability(address, False, timeout)
        time.sleep(self.policy['OSNetworkToHaltTime'])
        return result

    def _target_on_to_state(self, state, force):
        """Attempt to boot the node to a OS."""
        current = self.get_current_device_power_state()
        if current == 'On:bmc_on':
            if not self._graceful_os_halt():
                if not force:
                    return False
            current = self.get_current_device_power_state()
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
                    self._wait_for_network_availability(
                        self.os_credentials.address,
                        True, timeout)
        return result

    def _do_simple_bmc_reboot(self, state):
        """From a non-OS chassis on state reboot to new state."""
        result = self.bmc_access.set_chassis_state(self.bmc_credentials, state)
        if result and state in ['on', 'cycle']:
            timeout = self.policy['OSBootTimeoutSeconds']
            result = \
                self._wait_for_network_availability(self.os_credentials.address,
                                                    True, timeout)
        return result
