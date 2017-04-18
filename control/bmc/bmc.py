# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This defines the interface for BMC objects.
"""
from ..plugin import DeclareFramework


@DeclareFramework('bmc')
class Bmc(object):
    """Interface class for bmc classes."""
    def __init__(self):
        pass

    def get_chassis_state(self, remote_access_object):
        """Get the current chassis state for a node."""
        pass

    def set_chassis_state(self, remote_access_object, new_state):
        """Set the target chassis state for a node."""
        pass
