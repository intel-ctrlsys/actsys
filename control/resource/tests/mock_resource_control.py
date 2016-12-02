# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Interface for all resource control plugins.
"""
from ..resource_control import ResourceControl
from ...plugin.manager import PluginMetadataInterface


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'resource_control'

    def name(self):
        """Get the plugin instance name."""
        return 'mock'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return MockResourceControl()


class MockResourceControl(ResourceControl):
    """Interface for resource control classes."""
    def __init__(self):
        super(ResourceControl, self).__init__()
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
