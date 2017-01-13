# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the Mock plugin for pdu access/control.
"""
import os
import unittest
from ..mock import PduMock
from ....plugin.manager import PluginManager
from ....utilities.remote_access_data import RemoteAccessData

class TestPduMock(unittest.TestCase):
    def setUp(self):
        self.pdu_file = os.path.sep + os.path.join('tmp', 'pdu_file')

    def test_persist_state(self):
        if os.path.exists(self.pdu_file):
            os.unlink(self.pdu_file)
        pdu = PduMock()
        connection = RemoteAccessData('127.0.0.1', 22, 'fsp', None)
        self.assertEqual('On', pdu.get_outlet_state(connection, '3'))
        pdu.set_outlet_state(connection, '3', 'Off')
        with self.assertRaises(RuntimeError):
            pdu.set_outlet_state(connection, '3', 'invalid_state')
        self.assertEqual('Off', pdu.get_outlet_state(connection, '3'))
        pdu = PduMock()
        self.assertEqual('Off', pdu.get_outlet_state(connection, '3'))