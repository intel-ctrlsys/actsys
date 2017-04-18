# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to mock BMC functionality.
"""
import os.path
import json
from ...plugin import DeclarePlugin
from ..bmc import Bmc


@DeclarePlugin('mock', 1000)
class BmcMock(Bmc):
    """Implement Bmc contract using IPMI."""
    def __init__(self):
        Bmc.__init__(self)
        self.state_change_delay = 5  # seconds
        self.__current_states = {}
        self.__persistent_file = os.path.join(os.path.sep, 'tmp', 'bmc_file')
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
