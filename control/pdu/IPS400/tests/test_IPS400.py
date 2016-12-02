# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the IPS400 PDU plugin for PDU access/control.
"""

import unittest
from mock import MagicMock, patch
from ..IPS400 import PluginMetadata, PduIPS400
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData
from ....os_remote_access.telnet.telnet import RemoteTelnetPlugin

IPS400_status = \
"Internet Power Switch v1.41d    Site ID: (undefined)\n" \
"Plug | Name           | Password    | Status | Boot/Seq. Delay | Default |\n" \
"-----+----------------+-------------+--------+-----------------+---------+\n" \
" 1   | (undefined)    | (undefined) |   ON   |     0.5 Secs    |   ON    |\n" \
" 2   | (undefined)    | (undefined) |   ON   |     0.5 Secs    |   ON    |\n" \
" 3   | (undefined)    | (undefined) |   ON   |     0.5 Secs    |   ON    |\n" \
" 4   | (undefined)    | (undefined) |   ON   |     0.5 Secs    |   ON    |\n" \
"-----+----------------+-------------+--------+-----------------+---------+\n"


class TestPduIPS400(unittest.TestCase):
    """Test the IPS400 pdu implementation."""

    def setUp(self):
        self.access = RemoteAccessData('', 0, '', '')

    def test_metadata_IPS400(self):
        manager = PluginManager()
        metadata = PluginMetadata()
        self.assertEqual('pdu', metadata.category())
        self.assertEqual('IPS400', metadata.name())
        self.assertEqual(100, metadata.priority())
        manager.add_provider(metadata)
        pdu = manager.factory_create_instance('pdu', 'IPS400')
        self.assertIsNotNone(pdu)

    def test_get_outlet_state(self):
        pdu = PduIPS400()
        pdu._execute_remote_telnet_command = MagicMock()
        MagicMock.return_value = 'Invalid command'
        with self.assertRaises(RuntimeError):
          pdu.get_outlet_state(self.access, 'On')
        MagicMock.return_value = IPS400_status
        self.assertEqual('On', pdu.get_outlet_state(self.access, '3'))

    def test_set_outlet_state(self):
        pdu = PduIPS400()
        with self.assertRaises(RuntimeError):
            pdu.set_outlet_state(self.access, '', 'invalid_state')
        pdu._execute_remote_telnet_command = MagicMock()
        MagicMock.return_value = 'Invalid command'
        with self.assertRaises(RuntimeError):
            pdu.set_outlet_state(self.access, '4', 'On')
        MagicMock.return_value = IPS400_status
        pdu.set_outlet_state(self.access, '2', 'Off')

    @patch.object(RemoteTelnetPlugin, 'execute')
    def test_execute_remote_telnet_command(self, mock_telnet):
        pdu = PduIPS400()
        mock_telnet.return_value = IPS400_status
        pdu._execute_remote_telnet_command(self.access, '/S')
        mock_telnet.return_value = None
        with self.assertRaises(RuntimeError):
            pdu._execute_remote_telnet_command(self.access, '/S')



