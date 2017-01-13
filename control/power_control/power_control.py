# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Interface for all device power control plugins.
"""
from ..plugin import DeclareFramework


@DeclareFramework('power_control')
class PowerControl(object):
    """Interface for device power control classes."""
    def __init__(self, options=None):
        pass

    def set_device_power_state(self, target_state, force_on_failure=False):
        """Set the current power target.  One of 'On', 'Off', 'On:<bios>'"""
        pass

    def get_current_device_power_state(self):
        """Get the current device power state.  Returns one of 'On', 'Off',
           'On:on'"""
        pass
