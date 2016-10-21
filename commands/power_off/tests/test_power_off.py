"""
Test the PowerOffCommand.
"""
import unittest
from ctrl.commands.power_off import PowerOffCommand


class TestPowerOnCommand(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""

    def setUp(self):
        self.node_name = "knl-123"
        self.power_off = PowerOffCommand(self.node_name)

    def test_execute(self):
        """Stub test, please update me"""

        self.assertEqual(self.power_off.execute().message, "Success: Power Off {}".format(self.node_name))


if __name__ == '__main__':
    unittest.main()
