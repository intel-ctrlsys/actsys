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
    def __init__(self):
        ResourceControl.__init__(self)
        self.return_value = True

    def remove_nodes_from_resource_pool(self, node_list):
        """Remove the specified list of nodes from the cluster resource pool"""
        return 0, 'Succeeded in removing nodes ' + str(node_list) + \
            ' from the cluster resource pool!'

    def add_nodes_to_resource_pool(self, node_list):
        """Add the specified list of nodes to the cluster resource pool"""
        return 0, 'Succeeded in adding node ' + str(node_list) + \
            ' back to the cluster resource pool!'

    def check_nodes_state(self, node_list):
        """Check the state of the specified list of nodes"""
        return self.return_value, "idle"

    def check_resource_manager_running(self):
        """Check whether the resource manager is running"""
        return self.return_value
