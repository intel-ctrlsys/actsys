# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Common functionality for resource control plugins.
"""
import os
from ..utilities import Utilities


class ResourceControlComm:

    def _remove_nodes_alloc(self):
        """
        Handle the situation where a list of nodes are in alloc state when
        removing the nodes from cluster resource pool
        """
        return 'Running jobs, cannot be removed!'

    def _remove_nodes_drain(self):
        """
        Handle the situation where a list of nodes are in drain state when
        removing the nodes from cluster resource pool
        """
        return 'Had already been removed!'

    def _remove_nodes_abnormal_state(self, state):
        """
        Handle the situation where a node is in other states when removing the
        nodes from cluster resource pool
        """
        return 'In ' + state + ' state, cannot be removed!'

    def remove_nodes_help(self, state, parse_func, remove_func):
        ret = 0
        lines = state.split(os.linesep)
        res_list = list()
        res_list.append(['NODELIST', 'RESULT'])
        for i in range(2, len(lines)):
            nodes, current_state = parse_func(lines[i].split())
            if nodes is None:
                continue
            if 'idle' == current_state:
                message = remove_func(nodes)
                if 'Failed' in message:
                    ret = 1
            elif 'alloc' == current_state:
                message = self._remove_nodes_alloc()
            elif 'drain' == current_state:
                message = self._remove_nodes_drain()
            else:
                message = self._remove_nodes_abnormal_state(current_state)
            res_list.append([nodes, message])
        return ret, os.linesep + Utilities.print_nested_list(res_list)

    def _add_nodes_alloc(self):
        """
        Handle the situation where a list of nodes are in alloc state when
        adding the nodes back to cluster resource pool
        """
        return 'Running job, already in resource pool!'

    def _add_nodes_idle(self):
        """
        Handle the situation where a list of nodes are in idle state when
        adding the nodes back to cluster resource pool
        """
        return 'Already in resource pool!'

    def _add_nodes_abnormal_state(self, state):
        """
        Handle the situation where a list of nodes are in other states
        when adding the nodes back to cluster resource pool
        """
        return 'In ' + state + ' state, cannot be added'

    def add_nodes_help(self, state, parse_func, add_func):
        """
        Add the specified list of nodes back to the cluster resource pool
        """
        ret = 0
        lines = state.split(os.linesep)
        res_list = list()
        res_list.append(['NODELIST', 'RESULT'])
        for i in range(2, len(lines)):
            nodes, current_state = parse_func(lines[i].split())
            if nodes is None:
                continue
            if 'drain' == current_state:
                message = add_func(nodes)
                if 'Failed' in message:
                    ret = 1
            elif 'alloc' == current_state:
                message = self._add_nodes_alloc()
            elif 'idle' == current_state:
                message = self._add_nodes_idle()
            else:
                message = self._add_nodes_abnormal_state(current_state)
            res_list.append([nodes, message])
        return ret, os.linesep + Utilities.print_nested_list(res_list)