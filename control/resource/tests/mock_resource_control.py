# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Interface for all resource control plugins.
"""
from ..resource_control import ResourceControl
from ...plugin import DeclarePlugin


@DeclarePlugin('mock', 100)
class MockResourceControl(ResourceControl):
    """Interface for resource control classes."""
    def __init__(self, options=None):
        ResourceControl.__init__(self, options)
        self.return_value = True

    def remove_node_from_resource_pool(self, node_name):
        """Remove the specified node from the cluster resource pool"""
        return 0, 'Succeeded in removing node ' + node_name + ' from the cluster resource pool!'

    def add_node_to_resource_pool(self, node_name):
        """Add the specified node to the cluster resource pool"""
        return 0, 'Succeeded in adding node ' + node_name + ' back to the cluster resource pool!'

    def check_node_state(self, node_name):
        """Check the state of the specified node"""
        return self.return_value, "idle"

    def check_resource_manager_installed(self):
        """Check whether the resource manager is installed """
        return self.return_value
