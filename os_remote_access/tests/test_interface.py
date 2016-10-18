"""
Test the remote access interface fom completeness.
"""
from ctrl.os_remote_access.interface import Interface
import unittest


class TestInterface(unittest.TestCase):
    """Unit tests for the os_remote_access interface."""
    def test_interface(self):
        """All tests."""
        interface = Interface()
        interface.execute([], None)


if __name__ == '__main__':
    unittest.main()
