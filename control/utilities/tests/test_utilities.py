# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the OS and Network Utilities
"""
import getpass
import unittest
import subprocess
from ..utilities import Utilities


class TestGetOsUtilities(unittest.TestCase):
    """These should work even under docker simulation"""

    def mocked_call(self, args, stdin=None, stdout=None, stderr=None,
                    shell=False):
        """Fake a call to subprocess.call"""
        return 0

    def test_ping_check(self):
        """All tests are in this method."""
        utilities = Utilities()
        saved = subprocess.call
        subprocess.call = self.mocked_call
        self.assertEqual(True, utilities.ping_check("127.0.0.1"))
        subprocess.call = saved

    def test_capture(self):
        utilities = Utilities()
        stdout = utilities.execute_no_capture(['ls', '/someunknownrootfolder'])
        self.assertEqual(2, stdout)
        stdout, stderr = utilities.execute_with_capture(['ls', '/someunknownrootfolder'])
        self.assertEqual(None, stdout)
        result = '%s\n' % getpass.getuser()
        stdout, stderr = utilities.execute_with_capture(['whoami'])
        self.assertEqual(result, stdout)

    def test_execute_in_shell(self):
        utilities = Utilities()
        rv, output = utilities.execute_in_shell('whoami')
        self.assertEqual(0, rv)
        self.assertEqual(getpass.getuser() + '\n', output)
        rv1, result = utilities.execute_in_shell('ls /someunknownrootfolder')
        self.assertEqual(255, rv1)

if __name__ == '__main__':
    unittest.main()
