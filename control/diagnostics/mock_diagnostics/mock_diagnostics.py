#
#Copyright (c) 2017 Intel Corp.
#

"""
Interface for mock diagnostic tests plugins.
"""
from __future__ import print_function
from control.plugin import DeclarePlugin
from control.diagnostics.diagnostics import Diagnostics


@DeclarePlugin('mock', 100)
class MockDiagnostics(Diagnostics):
    """This class controls launching the mock diagnostic tests"""

    def __init__(self, **kwargs):
        Diagnostics.__init__(self, **kwargs)

    def launch_diags(self, device, bmc):
        """launches the diagnostic tests"""
        device_name = device.get("hostname")
        return "Diagnostics completed on node {}".format(device_name)
