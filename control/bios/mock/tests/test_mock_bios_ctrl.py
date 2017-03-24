# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the Mock plugin for bios access/control.
"""
import os
import unittest
from ..mock import MockNC
import tempfile

class TestBiosCtrlMock(unittest.TestCase):
    def setUp(self):
        self.bios_file = os.path.sep + os.path.join(tempfile.gettempdir(), 'bios_file')
        self.device = {'device_name': 'localhost'}
        self.bmc = None

    def test_persist_state(self):
        if os.path.exists(self.bios_file):
            os.unlink(self.bios_file)
        mock_nc = MockNC(args=None)
        self.assertTrue('No image found' in mock_nc.get_version(self.device, self.bmc))
        self.assertTrue('Bios for' in mock_nc.bios_update(self.device, self.bmc, 'test.bin'))
        self.assertTrue('test.bin' in mock_nc.get_version(self.device, self.bmc))

        mock_nc = MockNC(args=None)
        self.assertTrue(mock_nc.get_version(self.device, self.bmc))
