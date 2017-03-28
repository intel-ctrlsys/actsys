# # -*- coding: utf-8 -*-
# #
# # Copyright (c) 2016 Intel Corp.
# #
# """
# Test the slurm_resource_control plugin implementation.
# """
import unittest
from ....utilities.utilities import Utilities, SubprocessOutput
from mock import patch
from ..slurm_resource_control import SlurmResource


class TestSlurmResourceControl(unittest.TestCase):
    """Test the SlurmResource class."""

    def check_slurm_installed_stub(self, expected_value):
        sr = SlurmResource()
        result = sr.check_resource_manager_installed()
        self.assertEqual(result, expected_value)

    @patch.object(Utilities, "execute_subprocess")
    def test_check_slurm_installed_none(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(1, None, None)
        self.check_slurm_installed_stub(False)

    @patch.object(Utilities, "execute_subprocess")
    def test_check_slurm_installed_mock_succeed(self,
                                                mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION", '')
        self.check_slurm_installed_stub(True)

    @patch.object(Utilities, "execute_subprocess")
    def test_check_slurm_installed_mock_fail(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "MOCKED_RETURN", '')
        self.check_slurm_installed_stub(False)

    def _assert_return_message(self, rc, message,
                               rc_expected, message_expected):
        self.assertEqual(rc_expected, rc)
        self.assertEqual(message_expected, message)

    def _remove_from_resource_pool_stub(self, rc_expected, message_expected):
        sr = SlurmResource()
        rc, message = sr.remove_node_from_resource_pool("localhost")
        self._assert_return_message(rc, message, rc_expected, message_expected)

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_not_found(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      0    n/a", '')
        self._remove_from_resource_pool_stub(1, "Node localhost not found in SLURM!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_success(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    idle localhost\n"
                                                         "Success", 'Success')
        self._remove_from_resource_pool_stub(0, "Succeeded in removing node "
                                                "localhost from the cluster "
                                                "resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_not_found_multiple(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      0    n/a"
                                                         "shared*       up   infinite      0    n/a"
                                                         "normal       up   infinite      0    n/a", '')
        self._remove_from_resource_pool_stub(1, "Node localhost not found in SLURM!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_success_multiple(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    n/a\n"
                                                         "normal       up   infinite      1    idle localhost\n"
                                                         "shared*       up   infinite      1    n/a\n"
                                                         "Success", 'Success')
        self._remove_from_resource_pool_stub(0, "Succeeded in removing node localhost from the cluster "
                                                "resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_failure(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    idle localhost", '')
        self._remove_from_resource_pool_stub(2, "Failed in removing node "
                                                "localhost from the cluster "
                                                "resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_in_alloc(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    alloc localhost", '')
        self._remove_from_resource_pool_stub(3, "Currently, the node localhost "
                                                "is busy running job, it cannot"
                                                " be removed from the cluster "
                                                "resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_in_drain(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    drain localhost", '')
        self._remove_from_resource_pool_stub(4, "The node localhost has "
                                                "already been removed from the "
                                                "cluster resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_node_in_abnormal_state(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    unknown localhost", '')
        self._remove_from_resource_pool_stub(5, "The node localhost is in "
                                                "unknown state, not be able to "
                                                "remove it from the cluster "
                                                "resource pool!")

    def _add_to_resource_pool_stub(self, rc_expected, message_expected):
        sr = SlurmResource()
        rc, message = sr.add_node_to_resource_pool("localhost")
        self._assert_return_message(rc, message, rc_expected, message_expected)

    @patch.object(Utilities, "execute_subprocess")
    def test_add_node_not_found(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      0    n/a", '')
        self._add_to_resource_pool_stub(1, "Node localhost not found in SLURM!")

    @patch.object(Utilities, "execute_subprocess")
    def test_add_node_success(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    drain localhost\n"
                                                         "Success", 'Success')
        self._add_to_resource_pool_stub(0, "Succeeded in adding node localhost "
                                           "back to the cluster resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_add_node_failure(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    drain localhost", '')
        self._add_to_resource_pool_stub(6, "Failed in adding node localhost "
                                           "back to the cluster resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_add_node_in_alloc(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    alloc localhost", '')
        self._add_to_resource_pool_stub(7, "Currently, the node localhost is "
                                           "busy running job, it is already in "
                                           "the cluster resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_add_node_in_idle(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    idle localhost", '')
        self._add_to_resource_pool_stub(8, "The node localhost is already in "
                                           "the cluster resource pool!")

    @patch.object(Utilities, "execute_subprocess")
    def test_add_node_in_abnormal_state(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    unknown localhost", '')
        self._add_to_resource_pool_stub(9, "The node localhost is in unknown "
                                           "state, not be able to add it back "
                                           "to the cluster resource pool!")
