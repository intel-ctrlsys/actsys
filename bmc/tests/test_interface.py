"""
Tests for Interface to satisfy code coverage.
"""
import unittest
from ctrl.bmc.interface import Interface


class TestInterface(unittest.TestCase):
    """Tests for the BMC Interface class"""
    def setUp(self):
        """Common setup for tests."""
        self.interface = Interface()

    def test_interface(self):
        self.interface.get_chassis_state('127.0.0.1', 'admin', 'PASSWORD')
        self.interface.set_chassis_state('127.0.0.1', 'admin', 'PASSWORD', 'on')
