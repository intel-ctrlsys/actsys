# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Interface for Node Controllers specific bios flash/settings.
"""

from ..plugin import DeclareFramework


@DeclareFramework('bios')
class BiosControl(object):
    """Interface for Node controller type classes."""
    def __init__(self):
        pass

    def get_version(self, node, bmc):
        """Read the bios image info for a compute node"""
        pass

    def bios_update(self, node, bmc, image):
        """Update bios on a compute node"""
        pass
