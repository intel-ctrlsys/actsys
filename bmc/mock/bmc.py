# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to mock BMC functionality.
"""
import os.path
import json
from ctrl.plugin.manager import PluginMetadataInterface
from ctrl.bmc.bmc import Bmc


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        super(PluginMetadata, self).__init__()

    def category(self):
        """Get the plugin category"""
        return 'bmc'

    def name(self):
        """Get the plugin instance name."""
        return 'mock'

    def priority(self):
        """Get the priority of this name in this category."""
        return 1000

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return BmcMock(options)


class BmcMock(Bmc):
    """Implement Bmc contract using IPMI."""
    def __init__(self, options=None):
        super(BmcMock, self).__init__(options)
        self.state_change_delay = 5  # seconds
        self.__current_states = {}
        self.__persistent_file = os.path.sep + os.path.join('tmp', 'bmc_file')
        if os.path.exists(self.__persistent_file):
            self._load_bmc_file()
        self.set_failure = False

    def get_chassis_state(self, remote_access):
        """Get the current power state of the node chassis as a boolean."""
        if remote_access.address in self.__current_states:
            return self.__current_states[remote_access.address] == 'on'
        else:
            self.__current_states[remote_access.address] = 'off'
            self._save_bmc_file()
            return False

    def set_chassis_state(self, remote_access, new_state):
        """Set the chassis to a new state."""
        states = {'off': 'off', 'on': 'on', 'cycle': 'on', 'bios': 'on',
                  'efi': 'on', 'hdd': 'on', 'pxe': 'on', 'cdrom': 'on',
                  'removable': 'on'}
        if new_state not in states:
            raise RuntimeError('An illegal BMC state was attempted: %s' %
                               new_state)
        self.__current_states[remote_access.address] = states[new_state]
        self._save_bmc_file()
        return not self.set_failure

    def _load_bmc_file(self):
        """Loads the bmc file from disk."""
        file_obj = open(self.__persistent_file)
        self.__current_states = json.load(file_obj)
        file_obj.close()

    def _save_bmc_file(self):
        """Saves the bmc file to disk."""
        file_obj = open(self.__persistent_file, 'w')
        json.dump(self.__current_states, file_obj)
        file_obj.close()
