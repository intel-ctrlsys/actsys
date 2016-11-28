# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Interface for all resource control plugins.
"""


class ResourceControl(object):
    """Interface for resource control classes."""
    def __init__(self):
        pass

    def remove_node_from_resource_pool(self, node_name):
        """Remove the specified node from the cluster resource pool"""
        pass

    def add_node_to_resource_pool(self, node_name):
        """Add the specified node to the cluster resource pool"""
        pass

    def check_node_state(self, node_name):
        """Check the state of the specified node"""
        pass

    def check_resource_manager_installed(self):
        """Check whether the resource manager is installed """
        pass
