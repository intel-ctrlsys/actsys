# # -*- coding: utf-8 -*-
# #
# # Copyright (c) 2016 Intel Corp.
# #
# """
# Test the slurm_resource_control plugin implementation.
# """
import unittest
from ....utilities.utilities import Utilities
from mock import patch
from ..slurm_resource_control import SlurmResource
from ..slurm_resource_control import PluginMetadata


class TestSlurmPluginMetadata(unittest.TestCase):
    """Test the Slurm PluginMetadata class."""
    def test_slurm_plugin(self):
        slurmPlugin = PluginMetadata()
        self.assertEqual("resource_control", slurmPlugin.category())
        self.assertEqual("slurm_resource_control", slurmPlugin.name())
        self.assertEqual(100, slurmPlugin.priority())
        self.assertIsNotNone(slurmPlugin.create_instance())


class TestSlurmResourceControl(unittest.TestCase):
    """Test the SlurmResource class."""
    def check_slurm_installed_stub(self, expected_value):
        sr = SlurmResource()
        result = sr.check_resource_manager_installed()
        self.assertEqual(result, expected_value)

    @patch.object(Utilities, "execute_with_capture")
    def test_check_slurm_installed_none(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = None, None
        self.check_slurm_installed_stub(False)

    @patch.object(Utilities, "execute_with_capture")
    def test_check_slurm_installed_mock_succeed(self,
                                                mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION", ''
        self.check_slurm_installed_stub(True)

    @patch.object(Utilities, "execute_with_capture")
    def test_check_slurm_installed_mock_fail(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "MOCKED_RETURN", ''
        self.check_slurm_installed_stub(False)

    def _assert_return_message(self, rc, message,
                               rc_expected, message_expected):
        self.assertEqual(rc_expected, rc)
        self.assertEqual(message_expected, message)

    def _remove_from_resource_pool_stub(self, rc_expected, message_expected):
        sr = SlurmResource()
        rc, message = sr.remove_node_from_resource_pool("localhost")
        self._assert_return_message(rc, message, rc_expected, message_expected)

    @patch.object(Utilities, "execute_with_capture")
    def test_remove_node_not_found(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      0    n/a", ''
        self._remove_from_resource_pool_stub(1, "Node localhost not found!")

    @patch.object(Utilities, "execute_with_capture")
    def test_remove_node_success(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    idle " \
                                                 "localhost\nSuccess", 'Success'
        self._remove_from_resource_pool_stub(0, "Succeeded in removing node "
                                                "localhost from the cluster "
                                                "resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_remove_node_failure(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    idle " \
                                                 "localhost", ''
        self._remove_from_resource_pool_stub(2, "Failed in removing node "
                                                "localhost from the cluster "
                                                "resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_remove_node_in_alloc(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    alloc " \
                                                 "localhost", ''
        self._remove_from_resource_pool_stub(3, "Currently, the node localhost "
                                                "is busy running job, it cannot"
                                                " be removed from the cluster "
                                                "resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_remove_node_in_drain(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    drain " \
                                                 "localhost", ''
        self._remove_from_resource_pool_stub(4, "The node localhost has "
                                                "already been removed from the "
                                                "cluster resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_remove_node_in_abnormal_state(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    unknown " \
                                                 "localhost", ''
        self._remove_from_resource_pool_stub(5, "The node localhost is in "
                                                "unknown state, not be able to "
                                                "remove it from the cluster "
                                                "resource pool!")

    def _add_to_resource_pool_stub(self, rc_expected, message_expected):
        sr = SlurmResource()
        rc, message = sr.add_node_to_resource_pool("localhost")
        self._assert_return_message(rc, message, rc_expected, message_expected)

    @patch.object(Utilities, "execute_with_capture")
    def test_add_node_not_found(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      0    n/a", ''
        self._add_to_resource_pool_stub(1, "Node localhost not found!")

    @patch.object(Utilities, "execute_with_capture")
    def test_add_node_success(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    drain " \
                                                 "localhost\nSuccess", 'Success'
        self._add_to_resource_pool_stub(0, "Succeeded in adding node localhost "
                                           "back to the cluster resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_add_node_failure(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    drain " \
                                                 "localhost", ''
        self._add_to_resource_pool_stub(6, "Failed in adding node localhost "
                                           "back to the cluster resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_add_node_in_alloc(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    alloc " \
                                                 "localhost", ''
        self._add_to_resource_pool_stub(7, "Currently, the node localhost is "
                                           "busy running job, it is already in "
                                           "the cluster resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_add_node_in_idle(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    idle " \
                                                 "localhost", ''
        self._add_to_resource_pool_stub(8, "The node localhost is already in "
                                           "the cluster resource pool!")

    @patch.object(Utilities, "execute_with_capture")
    def test_add_node_in_abnormal_state(self, mock_execute_with_capture):
        mock_execute_with_capture.return_value = "PARTITION AVAIL  " \
                                                 "TIMELIMIT  NODES  STATE " \
                                                 "NODELIST\n" \
                                                 "debug*       up   " \
                                                 "infinite      1    unknown " \
                                                 "localhost", ''
        self._add_to_resource_pool_stub(9, "The node localhost is in unknown "
                                           "state, not be able to add it back "
                                           "to the cluster resource pool!")