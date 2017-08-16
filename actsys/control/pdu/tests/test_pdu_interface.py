# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for Interface to satisfy code coverage.
"""
import unittest
from ..pdu_interface import PDUInterface
from ...utilities.remote_access_data import RemoteAccessData


class TestPdu(PDUInterface):
    def get_outlet_state(self, connection, outlet):
        return super(TestPdu, self).get_outlet_state(outlet, connection)

    def set_outlet_state(self, connection, outlet, new_state):
        return super(TestPdu, self).set_outlet_state(connection, outlet, new_state)

class TestPDUInterface(unittest.TestCase):
    """Tests for the PDU Interface class"""
    def setUp(self):
        """Common setup for tests."""
        self.interface = TestPdu()

    def test_interface(self):
        connection = RemoteAccessData('', '', '', None)
        self.interface.get_outlet_state(connection, '3')
        self.interface.set_outlet_state(connection, '3', 'on')
