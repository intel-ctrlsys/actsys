# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Implements a power_control plugin for controlling nodes.
"""
from __future__ import print_function
from ...plugin import DeclarePlugin
from ..power_control import PowerControl


@DeclarePlugin('rest_power', 100)
class RestPower(PowerControl):
    """This class controls node power.
    """
    def __init__(self, **kwargs):
        """Will throw is bad or missing data is passed in options."""
        PowerControl.__init__(self, kwargs)
        self.__options = kwargs
        if self.__options is None or self.__options == dict():
            raise RuntimeError('The options parameter to this class must not '
                               'be None!')
        self._parse_options()

    def get_current_device_power_state(self):
        """
        Get the current device power state. Returns one of 'On', 'Off',
        'On:bmc_on'
        """
        return self.bmc_access.get_chassis_state(self.bmc_credentials)

    def set_device_power_state(self, target_state, force_on_failure=False):
        """
        Set the current power target.  One of 'On', 'Off', 'On:<bmc_state>'
        """
        state = {'On': 'On', 'Off': 'Off', 'On:bmc_on': 'cycle'}
        return self.bmc_access.set_chassis_state(self.bmc_credentials,
                                                 state[target_state])

    def _parse_options(self):
        """Parse the options data contract."""
        self.device_type = self.__options.get('device_type')
        if self.device_type not in ['node', 'compute', 'service']:
            raise(RuntimeError('NodePower controller used on a non-node type '
                               'device!'))
        self.bmc_credentials, self.bmc_access = self.__options['bmc']
        if self.bmc_credentials is None:
            raise RuntimeError('The BMC credentials object passed was None!')
        if self.bmc_access is None:
            raise RuntimeError('The BMC access object passed was None!')
