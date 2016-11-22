# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to the IPS400 pdu
"""

from ...plugin.manager import PluginMetadataInterface
from ..pdu_interface import PDUInterface
from ...os_remote_access.telnet.telnet import RemoteTelnetPlugin


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        PluginMetadataInterface.__init__(self)

    def category(self):
        """Get the plugin category"""
        return 'pdu'

    def name(self):
        """Get the plugin instance name."""
        return 'IPS400'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return PduIPS400(options)


class PduIPS400(PDUInterface):
    """
    Implement pdu contract using IPS400
    """
    def __init__(self, options=None):
        super(PduIPS400, self).__init__(options=None)

    def get_outlet_state(self, connection, outlet):
        """
        Get the current power state of the node outlet as a boolean
        """
        output = self._execute_remote_telnet_command('/S', connection)
        lines = output.split('\n')
        value = None
        for line in lines:
            print line + "\n\n\n"
            if line.strip().startswith(outlet):
                value = line.strip().split('|')[3].strip()
                break
        if value is None:
            raise RuntimeError('Failed to retrieve'
                               ' IPS400 outlet %s state' % outlet)
        return value

    def set_outlet_state(self, connection, outlet, new_state):
        """
        Set the outlet to a new state.
        """
        if new_state not in self.valid_states:
            raise RuntimeError('Invalid PDU state requested')
        cmd = '/' + new_state.capitalize() + outlet + ',y'
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
