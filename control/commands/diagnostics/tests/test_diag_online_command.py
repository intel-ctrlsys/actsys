# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Test the diagnostics online command Plugin.
"""
from .. import DiagnosticsOnlineCommand
from .test_diag_command import TestDiagnosticsCommand


class TestDiagOnlineCommand(TestDiagnosticsCommand):
    def setUp(self):
        super(TestDiagOnlineCommand, self).setUp()
        self.diag_online = DiagnosticsOnlineCommand(self.node_name, self.configuration_manager,
                                                    self.mock_plugin_manager, None)

    def test_ret_msg(self):
        self.diag_manager_mock.launch_diags.return_value = 'Success'
        self.assertEqual(self.diag_online.execute().return_code, 0)
        self.diag_manager_mock.launch_diags.side_effect = Exception
        self.assertEqual(self.diag_online.execute().return_code, 1)
