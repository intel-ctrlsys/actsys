# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Interface for all resource control plugins.
"""

from ..plugin import DeclareFramework


@DeclareFramework('resource_control')
class ResourceControl(object):
    """Interface for resource control classes."""
    def __init__(self):
        pass

    def remove_nodes_from_resource_pool(self, node_list):
        """Remove the specified list of nodes from the cluster resource pool"""
        pass

    def add_nodes_to_resource_pool(self, node_list):
        """Add the specified list of nodes to the cluster resource pool"""
        pass

    def check_nodes_state(self, node_list):
        """Check the states of the specified list of nodes"""
        pass

    def check_resource_manager_running(self):
        """Check whether the resource manager is running """
        pass
