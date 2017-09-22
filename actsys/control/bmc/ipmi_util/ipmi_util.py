# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Plugin to talk to the BMC using IPMI versions 1.5 and 2.0.
"""
from time import sleep
from ...plugin import DeclarePlugin
from ...utilities.utilities import Utilities
from ..bmc import Bmc


@DeclarePlugin('ipmi_util', 100)
class BmcIpmiUtil(Bmc):
    """Implement Bmc contract using IPMI."""

    def __init__(self):
        Bmc.__init__(self)
        self.utilities = Utilities()
        self.tool = 'ipmiutil'
        self.name_to_find = 'chassis_power'
        self.mandatory_bmc_wait_seconds = 10

    def get_chassis_state(self, remote_access_object):
        """Get the current power state of the node chassis as a boolean."""
        command = self._build_power_command(remote_access_object.address,
                                            remote_access_object.username,
                                            remote_access_object.identifier,
                                            'status')
        subprocess_result = self.utilities.execute_subprocess(command)
        if subprocess_result.return_code != 0 or subprocess_result.stdout is None:
            # TODO: Integrate Logger, and log this failure information
            # TODO: Sometimes the ipmi tool fails, even though it actually succeeds. Root cause this, or double check.
            raise RuntimeError('Failed to execute "{}"! Command: {} stdout: {} stderr: {}'
                               .format(self.tool, command, subprocess_result.stdout, subprocess_result.stderr))
        lines = subprocess_result.stdout.decode().split('\n')
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

    def set_chassis_state(self, remote_access_object, new_state):
        """Set the chassis to a new state."""
        command = self._build_power_command(remote_access_object.address,
                                            remote_access_object.username,
                                            remote_access_object.identifier,
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
            command = [self.tool, 'health', '-N', str(address), '-U', str(user), '-V',
                       '4', '-P', str(password)]
            return command
        else:
            command = [self.tool, 'power', '-N', str(address), '-U', str(user), '-V', '4',
                       '-w', '-P', str(password), cmd_map[cmd]]
            return command
