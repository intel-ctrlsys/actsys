# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests to test the interface for resource_control.
"""
import unittest
from ..resource_control import ResourceControl


class TestResourceControl(unittest.TestCase):
    """class to run the UT for the resource_control interface."""
    def test_all_tests(self):
        """All tests."""
        interface = ResourceControl()
        interface.remove_node_from_resource_pool("localhost")
        interface.add_node_to_resource_pool("localhost")
        interface.check_node_state("localhost")
        interface.check_resource_manager_installed()
