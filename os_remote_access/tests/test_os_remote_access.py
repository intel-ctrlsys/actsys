# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the remote access interface fom completeness.
"""
from ctrl.os_remote_access.os_remote_access import OsRemoteAccess
import unittest


class TestInterface(unittest.TestCase):
    """Unit tests for the os_remote_access interface."""
    def test_interface(self):
        """All tests."""
        interface = OsRemoteAccess()
        interface.execute([], None)


if __name__ == '__main__':
    unittest.main()
