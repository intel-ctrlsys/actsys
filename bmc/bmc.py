# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This defines the interface for BMC objects.
"""


class Bmc(object):
    """Interface class for bmc classes."""
    def __init__(self, options=None):
        pass

    def get_chassis_state(self, remote_access_object):
        """Get the current chassis state for a node."""
        pass

    def set_chassis_state(self, remote_access_object, new_state):
        """Set the target chassis state for a node."""
        pass
