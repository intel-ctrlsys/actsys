# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Mock job launch plugin.
"""
import os
import json
import random
from ..plugin import DeclarePlugin
from .job_launch import JobLaunch
from ..utilities import Utilities


@DeclarePlugin('mock', 100)
class MockJobLaunch(JobLaunch):

    def __init__(self):
        self.job_list = ['mocked-job-1', 'mocked-job-2', 'mocked-job-3']
        self.state_list = ['running', 'pending', 'completed']
        self.node_list = ['mocked-node[1-10]', 'N/A', 'mocked-node[1-5]']

    def parse_job(self, job_script):
        try:
            with open(job_script, 'r') as f:
                job = json.load(f)
                return job
        except IOError as error:
            raise error

    def check_valid_job(self, job, node_count, nodes):
        if 'program' not in job:
            return 3, 'The job script has no executable!'
        num_node = None
        nodelist = None
        if node_count is not None:
            num_node = node_count
        elif 'node_count' in job:
            num_node = job['node_count']
        if nodes is not None:
            nodelist = ','.join(nodes)
        elif 'nodes' in job:
            nodelist = job['nodes']
        if num_node is None and nodelist is None:
            return 4, 'Please specify node requirements for the job'
        return None

    def launch_batch_job(self, job_script,
                         node_count=None, nodes=None, output_file=None):
        if job_script is None:
            return 1, 'Job script is mandatory!'
        try:
            job = self.parse_job(job_script)
        except IOError as error:
            return 2, error.strerror
        result = self.check_valid_job(job, node_count, nodes)
        if result:
            return result
        job_id = random.randint(1, 3)
        return 0, 'Job submitted successfully with id:mocked-job-' + str(job_id)

    def check_job_no_job_id_no_state(self, res_list):
        for i in range(0, 3):
            res_list.append([self.job_list[i], 'root',
                             self.node_list[i], self.state_list[i]])
        return 0, os.linesep + Utilities.print_nested_list(res_list)

    def check_job_no_job_id_with_state(self, state, res_list):
        if state not in self.state_list:
            return 1, 'No jobs found!'
        i = self.state_list.index(state)
        res_list.append([self.job_list[i], 'root', self.node_list[i], state])
        return 0, os.linesep + Utilities.print_nested_list(res_list)

    def check_job_with_job_id_no_state(self, job_id, res_list):
        if job_id not in self.job_list:
            return 1, 'No jobs found!'
        i = self.job_list.index(job_id)
        res_list.append([job_id, 'root', self.node_list[i], self.state_list[i]])
        return 0, os.linesep + Utilities.print_nested_list(res_list)

    def check_job_with_job_id_with_state(self, job_id, state, res_list):
        if job_id not in self.job_list or state not in self.state_list:
            return 1, 'No jobs found!'
        i = self.job_list.index(job_id)
        j = self.state_list.index(state)
        if i != j:
            return 1, 'No jobs found!'
        res_list.append([job_id, 'root', self.node_list[i], state])
        return 0, os.linesep + Utilities.print_nested_list(res_list)

    def check_job_metadata(self, job_id=None, state=None):
        res_list = list()
        res_list.append(['JOB_ID', 'USER_ID', 'NODELIST', 'STATE'])
        if job_id is None and state is None:
            return self.check_job_no_job_id_no_state(res_list)
        if job_id is None and state is not None:
            return self.check_job_no_job_id_with_state(state, res_list)
        if job_id is not None and state is None:
            return self.check_job_with_job_id_no_state(job_id, res_list)
        return self.check_job_with_job_id_with_state(job_id, state, res_list)

    def cancel_job(self, job_id):
        if job_id is None:
            return 1, 'Job id is mandatory!'
        if job_id not in self.job_list:
            return 1, 'No jobs found!'
        return 0, 'Job has been cancelled successfully!'