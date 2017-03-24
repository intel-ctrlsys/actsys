# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests to test the node controller interface.
"""
import unittest
from ..bios_control import BiosControl


class TestBiosControl(unittest.TestCase):
    """class to run the UT for the bios_control interface."""
    def test_all_tests(self):
        """All tests."""
        interface = BiosControl()
        interface.get_version(None, None)
        interface.bios_update(None, None, 'test.bin')
