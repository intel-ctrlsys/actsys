# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to the IPS400 pdu
"""

from ...plugin import DeclarePlugin
from ..pdu_interface import PDUInterface
from ...os_remote_access.telnet.telnet import RemoteTelnetPlugin


@DeclarePlugin('IPS400', 100)
class PduIPS400(PDUInterface):
    """
    Implement pdu contract using IPS400
    """
    def __init__(self):
        PDUInterface.__init__(self)

    def get_outlet_state(self, connection, outlet):
        """
        Get the current power state of the node outlet as a boolean
        """
        output = self._execute_remote_telnet_command('/S', connection)
        lines = output.split('\n')
        value = None
        for line in lines:
            if line.strip().startswith(outlet):
                value = line.strip().split('|')[3].strip()
                break
        if value is None:
            raise RuntimeError('Failed to retrieve'
                               ' IPS400 outlet %s state' % outlet)
        return value.capitalize()

    def set_outlet_state(self, connection, outlet, new_state):
        """
        Set the outlet to a new state.
        """
        if new_state not in self.valid_states:
            raise RuntimeError('Invalid PDU state requested')
        cmd = '/' + new_state.capitalize() + ' ' + outlet + ',y'
        result = self._execute_remote_telnet_command(cmd, connection)
        if 'Invalid' in result:
            raise RuntimeError('Failed to set outlet {0} '
                               'state to {1}'.format(outlet, new_state))

    @classmethod
    def _execute_remote_telnet_command(cls, remote_access_data, cmd):
        """
        Execute commands on the PDU
        """
        pdu_remote_access = RemoteTelnetPlugin()
        output = pdu_remote_access.execute(remote_access_data, cmd)
        if output is None:
            raise RuntimeError('Failed to execute command %s' % cmd)
        return output
