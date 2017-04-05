# # -*- coding: utf-8 -*-
# #
# # Copyright (c) 2016 Intel Corp.
# #
# """
# Test the mock_resource_control plugin implementation.
# """
import unittest
import os
import json
from ....utilities.utilities import Utilities
from ..mock_resource_control import MockResource


class TestMockResourceControl(unittest.TestCase):
    """Test the MockResource class."""
    def delete_mock_resource_file(self):
        file_path = os.path.join(os.path.sep, 'tmp', 'mock_resource')
        utility = Utilities()
        utility.execute_no_capture(['rm', '-rf', file_path])

    def tearDown(self):
        self.delete_mock_resource_file()

    def create_mock_resource_file(self, state):
        file_path = os.path.join(os.path.sep, 'tmp', 'mock_resource')
        nodes = {
            "localhost": {
                "state": state
            }
        }
        with open(file_path, 'w') as f:
            json.dump(nodes, f)

    def test_check_mock_installed(self):
        mock_resource = MockResource()
        self.assertEqual(True, mock_resource.check_resource_manager_installed())

    def _assert_return_message(self, rc, message,
                               rc_expected, message_expected):
        self.assertEqual(rc_expected, rc)
        self.assertEqual(message_expected, message)

    def _remove_from_resource_pool_stub(self, rc_expected,
                                        node_name, message_expected):
        mock_resource = MockResource()
        rc, message = mock_resource.remove_node_from_resource_pool(node_name)
        self._assert_return_message(rc, message, rc_expected, message_expected)

    def test_remove_node_file_not_found(self):
        self.delete_mock_resource_file()
        self._remove_from_resource_pool_stub(1, "localhost",
                                             "Node localhost not found!")

    def test_remove_node_node_not_found(self):
        self.create_mock_resource_file("idle")
        self._remove_from_resource_pool_stub(1, "localhost1",
                                             "Node localhost1 not found!")

    def test_remove_node_success(self):
        self.create_mock_resource_file("idle")
        self._remove_from_resource_pool_stub(0, "localhost",
                                                "Succeeded in removing node "
                                                "localhost from the cluster "
                                                "resource pool!")

    def test_remove_node_in_alloc(self):
        self.create_mock_resource_file("alloc")
        self._remove_from_resource_pool_stub(3, "localhost",
                                                "Currently, the node localhost "
                                                "is busy running job, it cannot"
                                                " be removed from the cluster "
                                                "resource pool!")

    def test_remove_node_in_drain(self):
        self.create_mock_resource_file("drain")
        self._remove_from_resource_pool_stub(4, "localhost",
                                                "The node localhost has "
                                                "already been removed from the "
                                                "cluster resource pool!")

    def test_remove_node_in_abnormal_state(self):
        self.create_mock_resource_file("unknown")
        self._remove_from_resource_pool_stub(5, "localhost",
                                                "The node localhost is in "
                                                "unknown state, not be able to "
                                                "remove it from the cluster "
                                                "resource pool!")

    def _add_to_resource_pool_stub(self, rc_expected, message_expected):
        mock_resource = MockResource()
        rc, message = mock_resource.add_node_to_resource_pool("localhost")
        self._assert_return_message(rc, message, rc_expected, message_expected)

    def test_add_node_not_found(self):
        self.delete_mock_resource_file()
        self._add_to_resource_pool_stub(1, "Node localhost not found!")

    def test_add_node_success(self):
        self.create_mock_resource_file("drain")
        self._add_to_resource_pool_stub(0, "Succeeded in adding node localhost "
                                           "back to the cluster resource pool!")

    def test_add_node_in_alloc(self):
        self.create_mock_resource_file("alloc")
        self._add_to_resource_pool_stub(7, "Currently, the node localhost is "
                                           "busy running job, it is already in "
                                           "the cluster resource pool!")

    def test_add_node_in_idle(self):
        self.create_mock_resource_file("idle")
        self._add_to_resource_pool_stub(8, "The node localhost is already in "
                                           "the cluster resource pool!")

    def test_add_node_in_abnormal_state(self):
        self.create_mock_resource_file("unknown")
        self._add_to_resource_pool_stub(9, "The node localhost is in unknown "
                                           "state, not be able to add it back "
                                           "to the cluster resource pool!")