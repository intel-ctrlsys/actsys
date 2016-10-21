# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to the BMC using IPMI versions 1.5 and 2.0.
"""
from time import sleep
from ctrl.plugin.manager import PluginMetadataInterface
from ctrl.utilities.utilities import Utilities
from ctrl.bmc.bmc import Bmc


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        PluginMetadataInterface.__init__(self)

    def category(self):
        """Get the plugin category"""
        return 'bmc'

    def name(self):
        """Get the plugin instance name."""
        return 'ipmi_util'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return BmcIpmiUtil(options)


class BmcIpmiUtil(Bmc):
    """Implement Bmc contract using IPMI."""
    def __init__(self, options=None):
        Bmc.__init__(self, options)
        self.utilities = Utilities()
        self.tool = 'ipmiutil'
        self.name_to_find = 'chassis_power'
        self.mandatory_bmc_wait_seconds = 10

    def get_chassis_state(self, remote_access):
        """Get the current power state of the node chassis as a boolean."""
        command = self._build_power_command(remote_access.address,
                                            remote_access.username,
                                            remote_access.identifier,
                                            'status')
        output = self.utilities.execute_with_capture(command)
        if output is None:
            raise RuntimeError('Failed to execute "%s"!' % self.tool)
        lines = output.split('\n')
        value = None
        for line in lines:
            if line.strip().startswith(self.name_to_find):
                value = line.strip().split('=')[1].strip()
                continue
        if value is None:
            raise RuntimeError('Failed to retrieve chassis power state!')
        # For stability with different BMC implementations...no way to check
        # stability dynamically in IPMI.
        sleep(self.mandatory_bmc_wait_seconds)
        return value == 'on'

    def set_chassis_state(self, remote_access, new_state):
        """Set the chassis to a new state."""
        command = self._build_power_command(remote_access.address,
                                            remote_access.username,
                                            remote_access.identifier,
                                            new_state)
        result = self.utilities.execute_no_capture(command)
        if result != 0:
            raise RuntimeError('Failed to execute "%s"!' % self.tool)
        # For stability with different BMC implementations...no way to check
        # stability dynamically in IPMI.
        sleep(self.mandatory_bmc_wait_seconds)
        return True

    def _build_power_command(self, address, user, password, cmd):
        """Build the beginning of an ipmiutil command"""
        cmd_map = {'off': '-d',        # Hard power off the node
                   'on': '-u',         # Boot to the default BIOS boot option
                   'cycle': '-c',      # Power cycles the node
                   'bios': '-b',       # Reboot to BIOS setup
                   'efi': '-e',        # Reboot to EFI shell
                   'hdd': '-h',        # reboot to primary HDD device
                   'pxe': 'p',         # Reboot to network PXE device
                   'cdrom': '-v',      # Reboot to optical media
                   'removable': '-f',  # Reboot to removable media (floppy)
                   'status': ''}       # Get the current chassis power state
        if cmd not in cmd_map:
            raise RuntimeError('Illegal command passed "%s"!' % cmd)
        if cmd == 'status':
            command = [self.tool, 'health', '-N', address, '-U', user, '-V',
                       '4', '-P', password]
            return command
        else:
            command = [self.tool, 'power', '-N', address, '-U', user, '-V', '4',
                       '-w', '-P', password, cmd_map[cmd]]
            return command
