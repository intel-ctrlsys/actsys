"""
Test the RemoteSshPlugin.
"""
import getpass
import unittest
import ctrl.os_remote_access.ssh.ssh
from ctrl.plugin.manager import PluginManager
from ctrl.utilities.remote_access_data import RemoteAccessData
from ctrl.utilities.utilities import Utilities


class MockUtilities(Utilities):
    """Mock class fake low level system call helpers."""
    def __init__(self):
        Utilities.__init__(self)
        self.returned_value = None

    def execute_no_capture(self, command):
        """Execute a command list suppressing output and returning the return
           code."""
        if self.returned_value is None:
            return 0
        else:
            return self.returned_value

    def execute_with_capture(self, command):
        """Execute a command list capturing output and returning the return
           code, stdout, stderr"""
        return self.returned_value

    def ping_check(self, address):
        """Check if a network address has a OS responding to pings."""
        if self.returned_value is None:
            return True
        else:
            return self.returned_value


class TestRemoteSshPlugin(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""
    def setUp(self):
        manager = PluginManager()
        metadata = ctrl.os_remote_access.ssh.ssh.PluginMetadata()
        manager.add_provider(metadata)
        self.remote = manager.factory_create_instance(metadata.category(),
                                                      metadata.name())
        self.remote.utilities = MockUtilities()  # Mocking
        self.access = RemoteAccessData('127.0.0.1', 22, getpass.getuser(), None)

    def test_plugin_metadata(self):
        """Test metadata."""
        meta = ctrl.os_remote_access.ssh.ssh.PluginMetadata()
        self.assertEqual('os_remote_access', meta.category())
        self.assertEqual('ssh', meta.name())
        self.assertEqual(100, meta.priority())
        self.assertIsNotNone(meta.create_instance())

    def test_execute_1(self):
        """Test the RemoteSshPlugin.execute() method."""
        rv1 = self.remote.execute(['whoami'], self.access)
        self.remote.utilities.returned_value = ''
        rv2, output = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual(0, rv1)
        self.assertEqual(0, rv2)

    def test_execute_2(self):
        """Test of execute part 2."""
        self.remote.utilities.returned_value = 0
        self.access.identifier = 'id'
        result = self.remote.execute(['whoami'], self.access)
        self.assertEqual(0, result)

    def test_execute_3(self):
        self.access.port = 22222
        self.remote.utilities.returned_value = ''
        result = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual((0, ''), result)

    def test_execute_4(self):
        self.access.port = 22222
        self.remote.utilities.returned_value = None
        result = self.remote.execute(['whoami'], self.access, capture=True)
        self.assertEqual((255, None), result)


if __name__ == '__main__':
    unittest.main()
