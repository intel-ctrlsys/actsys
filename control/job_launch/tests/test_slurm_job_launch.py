# # -*- coding: utf-8 -*-
# #
# # Copyright (c) 2017 Intel Corp.
# #
# """
# Test the slurm_job_launch plugin implementation.
# """
import unittest
from mock import patch
from ...utilities.utilities import Utilities, SubprocessOutput
from ..slurm_job_launch import SlurmJobLaunch


class TestSlurmJobLaunch(unittest.TestCase):
    """Test the SlurmJobLaunch class."""

    def test_launch_job_no_job_script(self):
        job = SlurmJobLaunch()
        ret = job.launch_batch_job(None)
        self.assertEqual(ret, (1, 'Job script is mandatory!'))

    @patch.object(Utilities, 'execute_subprocess')
    def test_launch_job_sbatch_error(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(2, '', 'sbatch error')
        job = SlurmJobLaunch()
        ret = job.launch_batch_job('test_script', node_count='1', nodes=
                                   'test_node', output_file='job_1.output')
        self.assertEqual(ret, (2, '\nsbatch error'))

    @patch.object(Utilities, 'execute_subprocess')
    def test_launch_job_succeed(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, 'Submitted job '
                                                         'successfully 1', '')
        job = SlurmJobLaunch()
        ret = job.launch_batch_job('test_script')
        self.assertEqual(ret[0], 0)
        self.assertEqual(ret[1], 'Job submitted successfully with id:1')

    @patch.object(Utilities, 'execute_subprocess')
    def test_check_job_sacct_disabled(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(1, '', 'Error happened!')
        job = SlurmJobLaunch()
        ret = job.check_job_metadata()
        self.assertEqual(ret[0], 1)
        self.assertTrue('Error happened!' in ret[1])

    @patch.object(Utilities, 'execute_subprocess')
    def test_check_job_sacct_enabled_no_job(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, 'line1\nline2\n', '')
        job = SlurmJobLaunch()
        ret = job.check_job_metadata(job_id='1', state='running')
        self.assertEqual(ret[0], 1)
        self.assertEqual(ret[1], 'No jobs found!')

    @patch.object(Utilities, 'execute_subprocess')
    def test_check_job_sacct_enabled_succeed(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, 'line1\nline2\n'
                                                         'line3\n', '')
        job = SlurmJobLaunch()
        ret = job.check_job_metadata(job_id='1', state='running')
        self.assertEqual(ret[0], 0)
        self.assertTrue('line1\nline2\nline3' in ret[1])

    def test_retrieve_job_no_job_id(self):
        job = SlurmJobLaunch()
        ret = job.retrieve_job_result(None)
        self.assertEqual(ret[0], 1)
        self.assertEqual(ret[1], 'Job ID is mandatory')

    @patch.object(Utilities, 'execute_subprocess')
    def test_retrieve_job_no_file(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, '', '')
        job = SlurmJobLaunch()
        ret = job.retrieve_job_result('1')
        self.assertEqual(ret, (1, 'Job output file does not exist!'))

    @patch.object(Utilities, 'execute_subprocess')
    def test_retrieve_with_file_failed(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(1, 'job_1.output',
                                                      'Error happened!')
        job = SlurmJobLaunch()
        ret = job.retrieve_job_result('1', output_file='job_1.output')
        self.assertEqual(ret, (1, 'Error happened!'))

    @patch.object(Utilities, 'execute_subprocess')
    def test_retrieve_with_file_succeed(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, 'pi=3.1415926', '')
        job = SlurmJobLaunch()
        ret = job.retrieve_job_result('1', output_file='job_1.output')
        self.assertEqual(ret, (0, 'pi=3.1415926'))

    def test_cancel_job_no_job_id(self):
        job = SlurmJobLaunch()
        ret = job.cancel_job(None)
        self.assertEqual(ret, (1, 'Job id is mandatory!'))

    @patch.object(Utilities, 'execute_subprocess')
    def test_cancel_job_none_zero_ret_code(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(1, '', 'Error happened!')
        job = SlurmJobLaunch()
        ret = job.cancel_job('1')
        self.assertEqual(ret, (1, 'No jobs found!'))

    @patch.object(Utilities, 'execute_subprocess')
    def test_cancel_job_fail(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, '', 'error happened!')
        job = SlurmJobLaunch()
        ret = job.cancel_job('1')
        self.assertEqual(ret, (1, '\nerror happened!'))

    @patch.object(Utilities, 'execute_subprocess')
    def test_cancel_job_succeed(self, mock_exec_sub):
        mock_exec_sub.return_value = SubprocessOutput(0, '', '')
        job = SlurmJobLaunch()
        ret = job.cancel_job('1')
        self.assertEqual(ret, (0, 'Job has been cancelled successfully!'))