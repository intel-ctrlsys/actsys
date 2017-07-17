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

    def check_slurm_running_stub(self, expected_value):
        sr = SlurmResource()
        result = sr.check_resource_manager_running()
        self.assertEqual(result, expected_value)

    @patch.object(Utilities, "execute_subprocess")
    def test_check_slurm_running_none(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(1, None, None)
        self.check_slurm_running_stub(False)

    @patch.object(Utilities, "execute_subprocess")
    def test_check_slurm_running_mock_succeed(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION", '')
        self.check_slurm_running_stub(True)

    @patch.object(Utilities, "execute_subprocess")
    def test_check_slurm_running_mock_fail(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "MOCKED_RETURN", '')
        self.check_slurm_running_stub(False)

    def _assert_return_message(self, rc, message,
                               rc_expected, message_expected):
        self.assertEqual(rc_expected, rc)
        self.assertTrue(message_expected in message)

    def _remove_from_resource_pool_stub(self, rc_expected, message_expected):
        sr = SlurmResource()
        rc, message = sr.remove_nodes_from_resource_pool("node[01-05]")
        self._assert_return_message(rc, message, rc_expected, message_expected)

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_nodes_success(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      5    idle node[01-05]\n"
                                                         "Success", 'Success')
        self._remove_from_resource_pool_stub(0, "Succeeded in removing!")

    @patch.object(Utilities, "execute_subprocess")
    def test_remove_nodes_failure_multiple_states(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    idle node01\n"
                                                         "debug*       up   infinite      2    alloc node[02-03]\n"
                                                         "debug*       up   infinite      1    drain node04\n"
                                                         "debug*       up   infinite      1    unknown node05", '')
        self._remove_from_resource_pool_stub(1, "Failed in removing!")

    def _add_to_resource_pool_stub(self, rc_expected, message_expected):
        sr = SlurmResource()
        rc, message = sr.add_nodes_to_resource_pool("node[01-05]")
        self._assert_return_message(rc, message, rc_expected, message_expected)

    @patch.object(Utilities, "execute_subprocess")
    def test_add_nodes_success(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      5    drain node[01-05]\n"
                                                         "Success", 'Success')
        self._add_to_resource_pool_stub(0, "Succeeded in adding!")

    @patch.object(Utilities, "execute_subprocess")
    def test_add_nodes_failure_multiple_states(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, "PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST\n"
                                                         "debug*       up   infinite      1    drain node01\n"
                                                         "debug*       up   infinite      2    alloc node[02-03]\n"
                                                         "debug*       up   infinite      1    idle node04\n"
                                                         "debug*       up   infinite      1    unknown node05", '')
        self._add_to_resource_pool_stub(1, "Failed in adding!")
