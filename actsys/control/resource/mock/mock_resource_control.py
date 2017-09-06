# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Implements a mock resource_control plugin for DFx.
"""
import os
import json
from ...plugin import DeclarePlugin
from ...cli import CommandInvoker
from ..resource_control import ResourceControl
from ..resource_control_common import ResourceControlComm
from datastore.filestore import FileStore
from datastore.datastore import logging
from datastore import DataStore
from ...utilities.utilities import Utilities


@DeclarePlugin('mock', 1000)
class MockResource(ResourceControl):
    """This class controls cluster resource using Mocked resource manager."""

    def __init__(self):
        """Constructor that load the mocked resource file if there is any"""
        ResourceControl.__init__(self)
        self.file_path = os.path.join(os.path.sep, 'tmp', 'mock_resource')
        self.command_invoker = CommandInvoker()
        self.configure_file = CommandInvoker.get_config_file_location()
        self.nodes = None
        self._load_mock_resource_file()
        self.resource_ctrl_helper = ResourceControlComm()

    def _read_file(self):
        with open(self.file_path, 'r') as f:
            try:
                self.nodes = json.load(f)
            except:
                self.nodes = None

    def _write_file(self):
        try:
            configure_manager = FileStore(self.configure_file, logging.DEBUG)
        except Exception as e:
            self.nodes = None
            return
        extractor = configure_manager
        nodes_metadata = extractor.get_devices_by_type('node')
        self.nodes = {}
        for node in nodes_metadata:
            self.nodes[node['hostname']] = {'state': 'drain'}
        self._save_mock_resource_file()

    def _load_mock_resource_file(self):
        """Load the mocked resource file, if not specified, create one"""
        if os.path.exists(self.file_path):
            self._read_file()
        else:
            self._write_file()

    def _save_mock_resource_file(self):
        """Save the current state to disk."""
        with open(self.file_path, 'w') as f:
            json.dump(self.nodes, f)

    def check_nodes_state(self, nodes):
        """
        Mock to check the states of the specified list of nodes
        """
        res_list = list()
        res_list.append(['NODELIST', 'STATE'])
        states = {}
        for node in nodes:
            current_state = self.nodes[node]['state']
            node_list = []
            if current_state in states:
                node_list = states[current_state]
            node_list.append(node)
            states[current_state] = node_list
        for state, node_list in states.items():
            res_list.append([DataStore.fold_devices(node_list), state])
        return 0, os.linesep + Utilities.print_nested_list(res_list)

    def _parse_columns(self, columns):
        return columns[0], columns[1]

    def _remove_nodes_idle(self, node_list):
        """
        Handle the situation where a list of nodes are in idle state when
        removing the nodes from cluster resource pool
        """
        nodes = self.command_invoker.datastore.expand_device_list(node_list)
        for node in nodes:
            self.nodes[node]['state'] = 'drain'
        self._save_mock_resource_file()
        return 'Succeeded in removing!'

    def remove_nodes_from_resource_pool(self, node_list):
        """
        Remove the specified list of nodes from the
        cluster resource pool for mock resource.
        """
        state = self.check_nodes_state(node_list)[1]
        return self.resource_ctrl_helper.remove_nodes_help(state,
                                                           self._parse_columns,
                                                           self._remove_nodes_idle)

    def _add_nodes_drain(self, node_list):
        """
        Handle the situation where a list of nodes are in drain state when
        adding the nodes back to cluster resource pool
        """
        nodes = self.command_invoker.datastore.expand_device_list(node_list)
        for node in nodes:
            self.nodes[node]['state'] = 'idle'
        self._save_mock_resource_file()
        return 'Succeeded in adding!'

    def add_nodes_to_resource_pool(self, node_list):
        """
        Add the specified list of nodes back to the cluster resource pool
        using mocked resource manager.
        """
        state = self.check_nodes_state(node_list)[1]
        return self.resource_ctrl_helper.add_nodes_help(state,
                                                        self._parse_columns,
                                                        self._add_nodes_drain)

    def check_resource_manager_running(self):
        """
        The Mocked resource manager is always running:
        """
        return True
