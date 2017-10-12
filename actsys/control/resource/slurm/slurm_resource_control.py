# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Implements a resource_control plugin for Slurm to control compute nodes.
"""
import os
from ...plugin import DeclarePlugin
from ..resource_control import ResourceControl
from ..resource_control_common import ResourceControlComm
from ...utilities.utilities import Utilities


@DeclarePlugin('slurm', 100)
class SlurmResource(ResourceControl):
    """This class controls cluster resource using Slurm resource manager."""

    def __init__(self):
        """Constructor that creates an utility and gets configuration"""
        ResourceControl.__init__(self)
        self.utilities = Utilities()
        self.num_column = 6
        self.node_column = 5
        self.state_column = 4
        self.resource_ctl_helper = ResourceControlComm()

    def check_nodes_state(self, node_list):
        """
        Check the states of the specified list of nodes using Slurm command
        """
        subprocess_result = self.utilities.execute_subprocess(['sinfo',
                                                               '-n', ','.join(node_list)])
        return 0, os.linesep + subprocess_result.stdout.decode()

    def _parse_columns(self, columns):
        if len(columns) != self.num_column:
            return None, None
        return columns[self.node_column], columns[self.state_column]

    def _remove_nodes_idle(self, node_list):
        """
        Handle the situation where a list of nodes are in idle state when
        removing the nodes from cluster resource pool
        """
        reason = "For service"
        subprocess_result = self.utilities.execute_subprocess(['scontrol', 'update',
                                                               'nodename=' + ','.join([node_list]),
                                                               'state=drain', 'reason=' + reason, '-vvvv'])
        if 'Success' in subprocess_result.stderr.decode():
            return 'Succeeded in removing!'
        return 'Failed in removing!'

    def remove_nodes_from_resource_pool(self, node_list):
        """
        Remove the specified list of nodes from the
        cluster resource pool using Slurm command.
        """
        state = self.check_nodes_state(node_list)[1]
        return self.resource_ctl_helper.remove_nodes_help(state,
                                                          self._parse_columns,
                                                          self._remove_nodes_idle)

    def _add_nodes_drain(self, node_list):
        """
        Handle the situation where a list of nodes are in drain state when
        adding the nodes back to cluster resource pool
        """
        reason = "Done with service"
        subprocess_result = self.utilities.execute_subprocess(['scontrol', 'update',
                                                               'nodename=' + ','.join([node_list]),
                                                               'state=resume', 'reason=' + reason, '-vvvv'])
        if 'Success' in subprocess_result.stderr.decode():
            return 'Succeeded in adding!'
        return 'Failed in adding!'

    def add_nodes_to_resource_pool(self, node_list):
        """
        Add the specified list of nodes back to the cluster resource pool
        using Slurm command.
        """
        state = self.check_nodes_state(node_list)[1]
        return self.resource_ctl_helper.add_nodes_help(state,
                                                       self._parse_columns,
                                                       self._add_nodes_drain)

    def check_resource_manager_running(self):
        """
        Check whether the Slurm resource manager is running using the 'sinfo'
        Slurm command:
        """
        try:
            subprocess_result = self.utilities.execute_subprocess(['sinfo'])
        except OSError:
            return False
        if subprocess_result.stdout is None:
            return False
        if 'PARTITION' in subprocess_result.stdout.decode():
            return True
        return False
