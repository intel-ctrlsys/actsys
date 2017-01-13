# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to the Raritan PX3 - 5180CR pdu
"""

from ...plugin import DeclarePlugin
from ..pdu_interface import PDUInterface
from ...os_remote_access.ssh.ssh import RemoteSshPlugin
from ...utilities.utilities import Utilities


@DeclarePlugin('Raritan_PX3-5180CR', 100)
class PduRaritanPX35180CR(PDUInterface):
    """Implement pdu contract using RaritanPX35180CR."""
    def __init__(self, options=None):
        PDUInterface.__init__(self, options)
        self.utilities = Utilities()

    def get_outlet_state(self, connection, outlet):
        """Get the current power state of the node outlet as a boolean."""
        cmd = 'show outlets ' + outlet
        output = self._execute_remote_pdu_command(connection, cmd)
        outlet_state = output.split()[-1]
        if outlet_state not in self.valid_states:
            raise RuntimeError('Failed to retrive RaritanPX35180CR '
                               'PDU outlet state')
        return outlet_state

    def set_outlet_state(self, connection, outlet, new_state):
        """Set the outlet to a new state."""
        if new_state not in self.valid_states:
            raise RuntimeError('Invalid PDU state requested')
        cmd = 'power outlets ' + outlet + ' ' + new_state.capitalize() + ' /y'
        result = self._execute_remote_pdu_command(connection, cmd)
        if "index" in result.lower() or "invalid" in result.lower():
            raise RuntimeError('Failed to set outlet {0} '
                               'state to {1}'.format(outlet, new_state))

    def _execute_remote_pdu_command(self, remote_access_data, cmd):
        """
        Execute commands on the PDU
        """
        pdu_remote_access = RemoteSshPlugin()
        ssh_cmd = pdu_remote_access._build_command([], remote_access_data)
        full_command = 'echo ' + cmd + ' | ' + ' '.join(ssh_cmd)
        rv, stdout = self.utilities.execute_in_shell(full_command)
        if rv != 0:
            raise RuntimeError('Failed to execute command %s' % cmd)
        return stdout
