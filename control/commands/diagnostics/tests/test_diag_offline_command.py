# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

"""
Test the diagnostics offline command Plugin.
"""
from .. import DiagnosticsOfflineCommand
from .test_diag_command import TestDiagnosticsCommand


class TestDiagOfflineCommand(TestDiagnosticsCommand):
    def setUp(self):
        super(TestDiagOfflineCommand, self).setUp()
        self.diag_offline = DiagnosticsOfflineCommand(self.node_name, self.configuration_manager,
                                                     self.mock_plugin_manager, None, test_name='sample')

    def test_ret_msg(self):
        self.assertEqual(self.diag_offline.execute().return_code, 0)
