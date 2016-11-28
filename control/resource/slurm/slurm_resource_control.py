# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements a resource_control plugin for Slurm to control compute nodes.
"""
from __future__ import print_function
import os
from ...plugin.manager import PluginMetadataInterface
from ..resource_control import ResourceControl
from ...utilities.utilities import Utilities


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'resource_control'

    def name(self):
        """Get the plugin instance name."""
        return 'slurm_resource_control'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return SlurmResource()


class SlurmResource(ResourceControl):
    """This class controls cluster resource using Slurm resource manager."""

    def __init__(self):
        """Constructor that creates an utility and gets configuration"""
        super(SlurmResource, self).__init__()
        self.utilities = Utilities()

    def _parse_node_state(self, output):
        lines = output.split(os.linesep)
        colums = lines[1].split()
        if 6 > len(colums):
            return None
        return colums[4]

    def check_node_state(self, node_name):
        """
        Check the status of the specified node using Slurm command
        """
        output = self.utilities.execute_with_capture(['sinfo', '-n', node_name])
        state = self._parse_node_state(output)
        if None == state:
            return 1, 'Node ' + node_name + ' not found!'
        return 0, state

    def _remove_node_idle(self, node_name):
        """
        Handle the situation where a node is in idle state when removing the
        node from cluster resource pool
        """
        reason = "For service"
        output = self.utilities.execute_with_capture(['scontrol', 'update',
                                                      'nodename=' + node_name,
                                                      'state=drain',
                                                      'reason=' + reason,
                                                      '-vvvv'])
        if 'Success' in output:
            message = 'Succeeded in removing node ' + node_name + \
                      ' from the cluster resource pool!'
            return 0, message
        message = 'Failed in removing node ' + node_name + \
                  ' from the cluster resource pool!'
        return 2, message

    def _remove_node_alloc(self, node_name):
        """
        Handle the situation where a node is in alloc state when removing the
        node from cluster resource pool
        """
        message = 'Currently, the node ' + node_name + ' is busy ' \
                  'running job, it cannot be removed from the cluster ' \
                  'resource pool!'
        return 3, message

    def _remove_node_drain(self, node_name):
        """
        Handle the situation where a node is in drain state when removing the
        node from cluster resource pool
        """
        message = 'The node ' + node_name + ' has already been removed ' \
                  'from the cluster resource pool!'
        return 4, message

    def _remove_node_abnormal_state(self, node_name, state):
        """
        Handle the situation where a node is in other states when removing the
        node from cluster resource pool
        """
        message = 'The node ' + node_name + ' is in ' + state + ' state, not ' \
                  'be able to remove it from the cluster resource pool!'
        return 5, message

    def remove_node_from_resource_pool(self, node_name):
        """
        Remove the specified node from the
        cluster resource pool using Slurm command.
        """
        ret, state = self.check_node_state(node_name)

        if 1 == ret:
            return ret, state

        if 'idle' == state:
            return self._remove_node_idle(node_name)

        if 'alloc' == state:
            return self._remove_node_alloc(node_name)

        if 'drain' == state:
            return self._remove_node_drain(node_name)

        return self._remove_node_abnormal_state(node_name, state)

    def _add_node_drain(self, node_name):
        """
        Handle the situation where a node is in drain state when adding the
        node back to cluster resource pool
        """
        reason = "Done with service"
        output = self.utilities.execute_with_capture(['scontrol', 'update',
                                                      'nodename=' + node_name,
                                                      'state=undrain',
                                                      'reason=' + reason,
                                                      '-vvvv'])
        if 'Success' in output:
            message = 'Succeeded in adding node ' + node_name + \
                      ' back to the cluster resource pool!'
            return 0, message
        message = 'Failed in adding node ' + node_name + \
                  ' back to the cluster resource pool!'
        return 6, message

    def _add_node_alloc(self, node_name):
        """
        Handle the situation where a node is in alloc state when adding the
        node back to cluster resource pool
        """
        message = 'Currently, the node ' + node_name + ' is busy ' \
                  'running job, it is already in the cluster resource pool!'
        return 7, message

    def _add_node_idle(self, node_name):
        """
        Handle the situation where a node is in idle state when adding the
        node back to cluster resource pool
        """
        message = 'The node ' + node_name + ' is already in the cluster ' \
                  'resource pool!'
        return 8, message

    def _add_node_abnormal_state(self, node_name, state):
        """
        Handle the situation where a node is in other states when adding the
        node back to cluster resource pool
        """
        message = 'The node ' + node_name + ' is in ' + state + ' state, not ' \
                  'be able to add it back to the cluster resource pool!'
        return 9, message

    def add_node_to_resource_pool(self, node_name):
        """
        Add the specified node back to the cluster resource pool
        using Slurm command.
        """
        ret, state = self.check_node_state(node_name)
        if 1 == ret:
            return ret, state

        if 'drain' == state:
            return self._add_node_drain(node_name)

        if 'alloc' == state:
            return self._add_node_alloc(node_name)

        if 'idle' == state:
            return self._add_node_idle(node_name)

        return self._add_node_abnormal_state(node_name, state)

    def check_resource_manager_installed(self):
        """
        Check whether the Slurm resource manager is installed using the 'sinfo'
        Slurm command:
        """
        output = self.utilities.execute_with_capture(['sinfo'])
        if None == output:
            return False
        if 'PARTITION' in output:
            return True
        return False