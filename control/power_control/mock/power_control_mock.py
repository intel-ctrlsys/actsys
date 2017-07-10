# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Power control mock class.
"""
import os.path
import json
from ...plugin import DeclarePlugin
from ..power_control import PowerControl


@DeclarePlugin('mock', 1000)
class PowerControlMock(PowerControl):
    """Plugin for mocking Power Control."""
    def __init__(self, **kwargs):
        options = kwargs
        PowerControl.__init__(self, options)
        self.device_list = options['device_list']
        self.current_state = "Off"

    def set_device_power_state(self, target_state, force_on_failure=False):
        """Set the current power target.  One of 'On', 'Off', 'On:<bios>'"""
        result_dict = {}
        for node in self.device_list:
            device_name = node.get("device_id")
            hostname = node['hostname']
            filename = device_name + "." + 'state'
            file_path = os.path.join(os.path.sep, 'tmp', filename)
            self._load_state(file_path)
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
            self._save_state(file_path)
            result_dict[hostname] = True
        return result_dict

    def get_current_device_power_state(self):
        """Get the current device power state.  Returns one of 'On', 'Off',
           'On:bmc_on'"""
        result_dict = {}
        for node in self.device_list:
            device_name = node.get("device_id")
            hostname = node['hostname']
            filename = device_name + "." + 'state'
            file_path = os.path.join(os.path.sep, 'tmp', filename)
            self._load_state(file_path)
            result_dict[hostname] = self.current_state
        return result_dict

    def _load_state(self, file_path):
        """Load state from disk or create default state is it doesn't exist."""
        if os.path.exists(file_path):
            file_ref = open(file_path)
            self.current_state = json.load(file_ref)
            file_ref.close()
        else:
            self._save_state(file_path)

    def _save_state(self, file_path):
        """Save the current state to disk."""
        file_ref = open(file_path, 'w')
        json.dump(self.current_state, file_ref)
        file_ref.close()

    @classmethod
    def _check_bmc_state(cls, bmc_target):
        """validate the bmc target."""
        target_list = ['bios', 'efi', 'hdd', 'pxe', 'cdrom', 'removable']
        if bmc_target not in target_list:
            raise RuntimeError('Bad BMC target: {}'.format(bmc_target))
