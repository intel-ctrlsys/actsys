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
from mock import patch
from ..utilities import Utilities


class TestGetOsUtilities(unittest.TestCase):
    """These should work even under docker simulation"""

    def setUp(self):
        self.utilities = Utilities()

    @patch("subprocess.call")
    def test_ping_check(self, mock_subprocess_call):
        """All tests are in this method."""
        mock_subprocess_call.return_value = 0
        self.assertEqual(True, self.utilities.ping_check("127.0.0.1"))
        self.assertEqual(False, self.utilities.ping_check("127.0.0.2"))
        self.assertEqual(True, self.utilities.ping_check("192.0.0.2"))

        mock_subprocess_call.return_value = 1
        self.assertEqual(True, self.utilities.ping_check("127.0.0.1"))
        self.assertEqual(False, self.utilities.ping_check("127.0.0.2"))
        self.assertEqual(False, self.utilities.ping_check("192.0.0.2"))

    @patch("subprocess.Popen")
    def test_execute_subprocess(self, mock_subprocess):
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.communicate.return_value = 'foo', 'var'
        result = self.utilities.execute_subprocess(['ls', '/some_unknown_folder'])
        self.assertEqual(0, result.return_code)
        self.assertEqual('foo', result.stdout)

        mock_subprocess.return_value.returncode = 5124
        mock_subprocess.return_value.communicate.return_value = None, 'jk'
        result = self.utilities.execute_subprocess(['ls', '/some_unknown_folder'])
        self.assertEqual(5124, result.return_code)
        self.assertEqual(None, result.stdout)
        self.assertEqual('jk', result.stderr)

        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.communicate.return_value = None, 'jk'
        result = self.utilities.execute_subprocess(['It', "Doesn't matter what is placed here."])
        self.assertEqual(1, result.return_code)
        self.assertEqual(None, result.stdout)
        self.assertEqual('jk', result.stderr)

    @patch("subprocess.call")
    def test_execute_no_capture(self, mock_subprocess_call):
        mock_subprocess_call.return_value = 1
        result = self.utilities.execute_no_capture(["foo"])
        self.assertEqual(1, result)

        mock_subprocess_call.return_value = 0
        result = self.utilities.execute_no_capture(["ls", '/junk_folder_of_doom'])
        self.assertEqual(0, result)

        mock_subprocess_call.return_value = 243
        result = self.utilities.execute_no_capture(["once", 'there', 'was', 'a', 'worm', 'it', 'liked',
                                                    'to', 'eat', 'dirt'])
        self.assertEqual(243, result)

    def test_execute_in_shell(self):
        rv, output = self.utilities.execute_in_shell('whoami')
        self.assertEqual(0, rv)
        self.assertEqual(getpass.getuser() + '\n', output)
        rv1, result = self.utilities.execute_in_shell('ls /someunknownrootfolder')
        self.assertEqual(255, rv1)


def mocked_call(self, args, stdin=None, stdout=None, stderr=None,
                shell=False):
    """Fake a call to subprocess.call"""
    return 0


if __name__ == '__main__':
    unittest.main()
