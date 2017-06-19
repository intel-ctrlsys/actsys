# # -*- coding: utf-8 -*-
# #
# # Copyright (c) 2016-2017 Intel Corp.
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
    def setUp(self):
        self.file_path = os.path.join(os.path.sep, 'tmp', 'mock_resource')
        self.utility = Utilities()

    def delete_mock_resource_file(self):
        self.utility.execute_no_capture(['rm', '-rf', self.file_path])

    def tearDown(self):
        self.delete_mock_resource_file()

    def create_mock_resource_file(self, nodes):
        with open(self.file_path, 'w') as f:
            json.dump(nodes, f)

    def test_check_mock_running(self):
        mock_resource = MockResource()
        self.assertEqual(True, mock_resource.check_resource_manager_running())

    def _assert_return_message(self, rc, message,
                               rc_expected, message_expected):
        self.assertEqual(rc_expected, rc)
        self.assertTrue(message_expected in message)

    def _remove_from_resource_pool_stub(self, rc_expected,
                                        node_list, message_expected):
        mock_resource = MockResource()
        rc, message = mock_resource.remove_nodes_from_resource_pool(node_list)
        self._assert_return_message(rc, message, rc_expected, message_expected)

    def test_remove_nodes_success_multi_states(self):
        nodes = {
            "node01": {
                "state": "idle"
            },
            "node02": {
                "state": "alloc"
            },
            "node03": {
                "state": "alloc"
            },
            "node04": {
                "state": "drain"
            },
            "node05": {
                "state": "unknown"
            },
        }
        self.create_mock_resource_file(nodes)
        self._remove_from_resource_pool_stub(0, "node[01-05]", "Succeeded in removing!")

    def _add_to_resource_pool_stub(self, rc_expected,
                                   node_list, message_expected):
        mock_resource = MockResource()
        rc, message = mock_resource.add_nodes_to_resource_pool(node_list)
        self._assert_return_message(rc, message, rc_expected, message_expected)

    def test_add_nodes_success_multi_states(self):
        nodes = {
            "node01": {
                "state": "idle"
            },
            "node02": {
                "state": "alloc"
            },
            "node03": {
                "state": "alloc"
            },
            "node04": {
                "state": "drain"
            },
            "node05": {
                "state": "unknown"
            },
        }
        self.create_mock_resource_file(nodes)
        self._add_to_resource_pool_stub(0, "node[01-05]", "Succeeded in adding!")
