# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ProcessListCommand.
"""
import unittest
from ctrl.commands.resource_pool_remove import ResourcePoolRemoveCommand


class TestProcessListCommand(unittest.TestCase):
    """Test case for the ProcessListCommand class."""

    def setUp(self):
        self.node_name = "knl-123"
        self.power_off = ResourcePoolRemoveCommand(self.node_name)

    def test_execute(self):
        """Stub test, please update me"""
        fmt = "Success: Resource Pool Remove {}"
        self.assertEqual(self.power_off.execute().message,
                         fmt.format(self.node_name))


if __name__ == '__main__':
    unittest.main()
