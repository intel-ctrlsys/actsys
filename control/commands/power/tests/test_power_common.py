# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the PowerOnCommand.
"""

from ..power_common import CommonPowerCommand
from .power_fixures import *
from ....pdu.mock.mock import PduMock


class TestPowerCommonCommand(PowerCommandsCommon):
    """Test case for the PowerOnNodeCommand class."""
    def setUp(self):
        super(TestPowerCommonCommand, self).setUp()
        self.command = CommonPowerCommand(self.command_options)
        self.command.device_name = 'test_pdu'

    def test_switch_pdu_no_outlet(self):
        self.args.outlet = None
        result = self.command.switch_pdu('On')
        self.assertEqual(1, result.return_code)

    def test_switch_pdu_state_change(self):
        self.args.outlet = 1
        result = self.command.switch_pdu('On')
        self.assertEqual(0, result.return_code)
        result1 = self.command.switch_pdu('Off')
        self.assertEqual(0, result1.return_code)

    def test_switch_pdu_no_state_change(self):
        self.args.outlet = 2
        result = self.command.switch_pdu('Off')
        self.assertEqual(0, result.return_code)
        result1 = self.command.switch_pdu('Off')
        self.assertEqual(0, result1.return_code)

    @patch.object(PduMock, 'get_outlet_state')
    def test_switch_pdu_get_failure(self, mock_get):
        self.args.outlet = 3
        mock_get.side_effect = RuntimeError('Failed to retrieve state')
        result = self.command.switch_pdu('Off')
        self.assertEqual(1, result.return_code)

    @patch.object(PduMock, 'set_outlet_state')
    def test_switch_pdu_set_failure(self, mock_set):
        self.args.outlet = 4
        mock_set.side_effect = RuntimeError('Failed to set outlet state')
        result = self.command.switch_pdu('Off')
        self.assertEqual(1, result.return_code)

if __name__ == '__main__':
    unittest.main()
