# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Power control mock class.
"""
import os.path
import json
from ctrl.plugin.manager import PluginMetadataInterface
from ctrl.power_control.power_control import PowerControl


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        PluginMetadataInterface.__init__(self)

    def category(self):
        """Get the plugin category"""
        return 'power_control'

    def name(self):
        """Get the plugin instance name."""
        return 'mock'

    def priority(self):
        """Get the priority of this name in this category."""
        return 1000

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return PowerControlMock(options)


class PowerControlMock(PowerControl):
    """Plugin for mocking Power Control."""
    def __init__(self, options=None):
        super(PowerControlMock, self).__init__(options)
        self.device_name = options['device_name']
        if options['device_type'] not in ['node', 'compute', 'service',
                                          'master', 'login']:
            raise RuntimeError('PowerControlMock invoked with a non-node type!')
        filename = self.device_name + "." + 'state'
        self.file_path = os.path.sep + os.path.join('tmp', filename)
        self.current_state = "Off"
        self._load_state()

    def set_device_power_state(self, target_state, force_on_failure=False):
        """Set the current power target.  One of 'On', 'Off', 'On:<bios>'"""
        fmt = 'Bad power command given: {}'
        parts = target_state.split(':')
        if parts[0] == 'Off' and len(parts) == 1:
            self.current_state = 'Off'
        elif parts[0] == 'On':
            if len(parts) == 1 and parts[0] == 'On':
                self.current_state = 'On:bmc_on'
            elif len(parts) == 2 and parts[1] == 'bmc_on':
                self.current_state = 'On:bmc_on'
            else:
                PowerControlMock._check_bmc_state(parts[1])
                self.current_state = 'On'
        else:
            raise RuntimeError(fmt.format(target_state))
        self._save_state()
        return True

    def get_current_device_power_state(self):
        """Get the current device power state.  Returns one of 'On', 'Off',
           'On:bmc_on'"""
        self._load_state()
        return self.current_state

    def _load_state(self):
        """Load state from disk or create default state is it doesn't exist."""
        if os.path.exists(self.file_path):
            file_ref = open(self.file_path)
            self.current_state = json.load(file_ref)
            file_ref.close()
        else:
            self._save_state()

    def _save_state(self):
        """Save the current state to disk."""
        file_ref = open(self.file_path, 'w')
        json.dump(self.current_state, file_ref)
        file_ref.close()

    @classmethod
    def _check_bmc_state(cls, bmc_target):
        """validate the bmc target."""
        target_list = ['bios', 'efi', 'hdd', 'pxe', 'cdrom', 'removable']
        if bmc_target not in target_list:
            raise RuntimeError('Bad BMC target: {}'.format(bmc_target))
