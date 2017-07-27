# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Interface for all diagnostic tests plugins.
"""
from control.plugin import DeclareFramework


@DeclareFramework('diagnostics')
class Diagnostics(object):
    """Interface for diagnostics classes."""
    def __init__(self, **options):
        """Init function"""
        pass

    def launch_diags(self, device, bmc):
        """launches the requested diagnostic test on the device"""
        pass
