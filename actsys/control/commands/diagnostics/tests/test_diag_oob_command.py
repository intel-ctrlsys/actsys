# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Test the diagnostics oob command Plugin.
"""
from .. import DiagnosticsOOBCommand
from .test_diag_command import TestDiagnosticsCommand


class TestDiagoobCommand(TestDiagnosticsCommand):
    def setUp(self):
        super(TestDiagoobCommand, self).setUp()
        self.diag_oob = DiagnosticsOOBCommand(self.node_name, self.configuration_manager,
                                                  self.mock_plugin_manager, None, test_name='sample')

    def test_ret_msg(self):
        self.assertEqual(self.diag_oob.execute().return_code, 0)
