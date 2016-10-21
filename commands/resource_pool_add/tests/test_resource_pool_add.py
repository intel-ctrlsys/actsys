"""
Test the ProcessListCommand.
"""
import unittest
from ctrl.commands.resource_pool_add import ResourcePoolAddCommand


class TestProcessListCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    def setUp(self):
        self.node_name = "knl-123"
        self.power_off = ResourcePoolAddCommand(self.node_name)

    def test_execute(self):
        """Stub test, please update me"""

        self.assertEqual(self.power_off.execute().message, "Success: Resource Pool Add {}".format(self.node_name))


if __name__ == '__main__':
    unittest.main()
