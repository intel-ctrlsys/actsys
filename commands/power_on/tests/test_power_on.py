"""
Test the PowerOffCommand.
"""
import unittest
from ctrl.commands.power_on import PowerOnCommand


class TestPowerOnCommand(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""

    def setUp(self):
        self.node_name = "knl-123"
        self.power_on = PowerOnCommand(self.node_name)

    def test_execute(self):
        """Stub test, please update me"""

        self.assertEqual(self.power_on.execute().message, "Success: Power On %{}".format(self.node_name))


if __name__ == '__main__':
    unittest.main()
