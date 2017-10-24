# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for Interface to satisfy code coverage.
"""
import unittest
from ..console_log import ConsoleLog


class TestInterfaceConsoleLog(unittest.TestCase):
    """Tests for the Console Log Interface class"""
    def setUp(self):
        """Common setup for tests."""
        self.interface = ConsoleLog()

    def test_interface(self):
        """Test the call of functions"""
        self.interface.start_log_capture('End', 'End')
        self.interface.stop_log_capture()
