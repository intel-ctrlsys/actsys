# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Implements a mock resource_control plugin for DFx.
"""
import os
import json
from ...plugin import DeclarePlugin
from ..resource_control import ResourceControl
from datastore.filestore import FileStore
from datastore.datastore import logging


@DeclarePlugin('mock', 1000)
class MockResource(ResourceControl):
    """This class controls cluster resource using Mocked resource manager."""

    def __init__(self, options=None):
        """Constructor that load the mocked resource file if there is any"""
        ResourceControl.__init__(self, options)
        self.file_path = os.path.join(os.path.sep, 'tmp', 'mock_resource')
        self.configure_file = "ctrl-config.json"
        self.nodes = None
        self._load_mock_resource_file()

    def _get_correct_configuration_file(self):
        """Resolve the configuration file if possible."""

        # Check for the file in the current working directory
        if os.path.isfile(self.configure_file):
            return os.path.join(os.path.curdir, self.configure_file)

        # check for file in ~/
        home = os.path.join(os.getenv('HOME'), self.configure_file)
        if os.path.isfile(home):
            return home

        # Check for the file in /etc/
        etc = '/etc/' + self.configure_file
        if os.path.isfile(etc):
            return etc

        return self.configure_file

    def _read_file(self):
        with open(self.file_path, 'r') as f:
            try:
                self.nodes = json.load(f)
            except:
                self.nodes = None

    def _write_file(self):
        try:
            configure_manager = FileStore(
                self._get_correct_configuration_file(), logging.DEBUG)
        except:
            self.nodes = None
            return
        extractor = configure_manager
        nodes_metadata = extractor.get_devices_by_type('node')
        self.nodes = {}
        for node in nodes_metadata:
            self.nodes[node['hostname']] = {'state': 'idle'}
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

    def check_node_state(self, node_name):
        """
        Mock to check the status of the specified node
        """
        if self.nodes is None or not (node_name in self.nodes):
            return 1, 'Node ' + node_name + ' not found!'
        return 0, self.nodes[node_name]['state']

    def _remove_node_idle(self, node_name):
        """
        Handle the situation where a node is in idle state when removing the
        node from cluster resource pool
        """
        self.nodes[node_name]['state'] = 'drain'
        message = 'Succeeded in removing node ' + node_name + \
                  ' from the cluster resource pool!'
        self._save_mock_resource_file()
        return 0, message

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
        cluster resource pool for mock resource.
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
        self.nodes[node_name]['state'] = 'idle'
        message = 'Succeeded in adding node ' + node_name + \
                  ' back to the cluster resource pool!'
        self._save_mock_resource_file()
        return 0, message

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
        using mocked resource manager.
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
        The Mocked resource manager is always installed:
        """
        return True
