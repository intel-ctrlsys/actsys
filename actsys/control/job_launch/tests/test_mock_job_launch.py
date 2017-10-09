# # -*- coding: utf-8 -*-
# #
# # Copyright (c) 2017 Intel Corp.
# #
# """
# Test the mock_job_launch plugin implementation.
# """
import unittest
import os
from ..mock_job_launch import MockJobLaunch


class TestMockJobLaunch(unittest.TestCase):
    """Test the MockJobLaunch class."""
    def setUp(self):
        self.file_path = os.path.dirname(os.path.realpath(__file__))

    def test_launch_job_no_job_script(self):
        mock_job = MockJobLaunch()
        ret = mock_job.launch_batch_job(None)
        self.assertEqual(ret, (1, 'Job script is mandatory!'))

    def test_launch_job_invalid_job_script(self):
        mock_job = MockJobLaunch()
        ret = mock_job.launch_batch_job('test_script')
        self.assertEqual(ret, (2, 'No such file or directory'))

    def test_launch_job_no_program(self):
        mock_job = MockJobLaunch()
        job_script = os.path.join(self.file_path, 'submit_script_no_program')
        ret = mock_job.launch_batch_job(job_script)
        self.assertEqual(ret, (3, 'The job script has no executable!'))

    def test_launch_job_no_node(self):
        mock_job = MockJobLaunch()
        job_script = os.path.join(self.file_path, 'submit_script_no_node')
        ret = mock_job.launch_batch_job(job_script)
        self.assertEqual(ret,
                         (4, 'Please specify node requirements for the job'))

    def test_launch_job_node_input(self):
        mock_job = MockJobLaunch()
        job_script = os.path.join(self.file_path, 'submit_script_no_node')
        ret = mock_job.launch_batch_job(job_script, node_count='1',
                                        nodes='test-node1')
        self.assertEqual(ret[0], 0)
        self.assertTrue('Job submitted successfully with id:mocked-job'
                        in ret[1])

    def test_launch_job_without_node_input(self):
        mock_job = MockJobLaunch()
        job_script = os.path.join(self.file_path, 'submit_script')
        ret = mock_job.launch_batch_job(job_script)
        self.assertEqual(ret[0], 0)
        self.assertTrue('Job submitted successfully with id:mocked-job'
                        in ret[1])

    def test_check_job_no_job_id_no_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata()
        self.assertEqual(ret[0], 0)

    def test_check_job_no_job_id_invalid_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(state='INVALID-STATE')
        self.assertEqual(ret, (1, 'No jobs found!'))

    def test_check_job_no_job_id_valid_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(state='pending')
        self.assertEqual(ret[0], 0)
        self.assertTrue('pending' in ret[1])

    def test_check_job_no_job_id_no_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata()
        self.assertEqual(ret[0], 0)

    def test_check_job_no_job_id_invalid_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(state='INVALID-STATE')
        self.assertEqual(ret, (1, 'No jobs found!'))

    def test_check_job_no_job_id_valid_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(state='pending')
        self.assertEqual(ret[0], 0)
        self.assertTrue('pending' in ret[1])

    def test_check_job_invalid_job_id_no_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(job_id='INVALID-job-id')
        self.assertEqual(ret, (1, 'No jobs found!'))

    def test_check_job_valid_job_id_no_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(job_id='mocked-job-1')
        self.assertEqual(ret[0], 0)
        self.assertTrue('mocked-job-1' in ret[1])

    def test_check_job_valid_job_id_invalid_state(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(job_id='mocked-job-1',
                                          state='INVALID-STATE')
        self.assertEqual(ret, (1, 'No jobs found!'))

    def test_check_job_job_id_state_not_match(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(job_id='mocked-job-1',
                                          state='completed')
        self.assertEqual(ret, (1, 'No jobs found!'))

    def test_check_job_job_id_state_match(self):
        mock_job = MockJobLaunch()
        ret = mock_job.check_job_metadata(job_id='mocked-job-1',
                                          state='running')
        self.assertEqual(ret[0], 0)
        self.assertTrue('running' in ret[1])

    def test_cancel_job_no_job_id(self):
        mock_job = MockJobLaunch()
        ret = mock_job.cancel_job(None)
        self.assertEqual(ret, (1, 'Job id is mandatory!'))

    def test_cancel_job_invalid_job_id(self):
        mock_job = MockJobLaunch()
        ret = mock_job.cancel_job('INVALID-job-id')
        self.assertEqual(ret, (1, 'No jobs found!'))

    def test_cancel_job_succeed(self):
        mock_job = MockJobLaunch()
        ret = mock_job.cancel_job('mocked-job-1')
        self.assertEqual(ret, (0, 'Job has been cancelled successfully!'))