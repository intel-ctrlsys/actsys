"""
Tests for the OS and Network Utilities
"""
import getpass
import unittest
from ctrl.utilities.utilities import Utilities


class TestGetOsUtilities(unittest.TestCase):
    """These should work even under docker simulation"""
    def test_get_os_utilities(self):
        """All tests are in this method."""
        utilities = Utilities()
        self.assertEqual(True, utilities.ping_check("127.0.0.1"))
        rv = utilities.execute_no_capture(['ls', '/someunknownrootfolder'])
        self.assertEqual(2, rv)
        rv = utilities.execute_with_capture(['ls', '/someunknownrootfolder'])
        self.assertEqual(None, rv)
        result = '%s\n' % getpass.getuser()
        self.assertEqual(result, utilities.execute_with_capture(['whoami']))


if __name__ == '__main__':
    unittest.main()
