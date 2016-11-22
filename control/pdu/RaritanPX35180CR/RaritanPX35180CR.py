# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to the Raritan PX3 - 5180CR pdu
"""

from ...plugin.manager import PluginMetadataInterface
from ..pdu_interface import PDUInterface
from ...os_remote_access.ssh.ssh import RemoteSshPlugin


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        PluginMetadataInterface.__init__(self)

    def category(self):
        """Get the plugin category"""
        return 'pdu'

    def name(self):
        """Get the plugin instance name."""
        return 'Raritan_PX3-5180CR'

    def priority(self):
        """Get the priority of this name in this category."""
        return 100

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return PduRaritanPX35180CR(options)


class PduRaritanPX35180CR(PDUInterface):
    """Implement pdu contract using RaritanPX35180CR."""
    def __init__(self, options=None):
        super(PduRaritanPX35180CR, self).__init__(options=None)

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
        if result is not None:
            raise RuntimeError('Failed to set outlet {0} '
                               'state to {1}'.format(outlet, new_state))

    @staticmethod
    def _execute_remote_pdu_command(remote_access_data, cmd):
        """
        Execute commands on the PDU
        """
        pdu_remote_access = RemoteSshPlugin()
        output = pdu_remote_access.execute([cmd], remote_access_data,
                                           capture=True, other=None)
        if output[0] != 0 or output[1] is None:
            raise RuntimeError('Failed to execute command %s' % cmd)
        return output[1]
