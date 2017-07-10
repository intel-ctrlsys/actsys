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
        return self.bmc_plugin.get_chassis_state(self.__options)

    def set_device_power_state(self, target_state, force_on_failure=False):
        """
        Set the current power target.  One of 'On', 'Off', 'On:<bmc_state>'
        """
        state = {'On': 'On', 'Off': 'Off', 'On:bmc_on': 'cycle'}
        return self.bmc_plugin.set_chassis_state(self.__options,
                                                 state[target_state])

    def _parse_options(self):
        """Parse the options"""
        plugin_manager = self.__options['plugin_manager']
        bmc_list = self.__options['bmc_list']
        try:
            bmc_access_type = bmc_list[0].get("access_type", None)
        except IndexError:
            raise RuntimeError('BMC list cannot be empty')
        if bmc_access_type:
            self.bmc_plugin = plugin_manager.create_instance('bmc', bmc_access_type)
        else:
            raise RuntimeError('BMC access type cannot be None')
