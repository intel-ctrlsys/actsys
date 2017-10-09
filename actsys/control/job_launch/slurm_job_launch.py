# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
SLURM job launch plugin.
"""
import os
from ..plugin import DeclarePlugin
from .job_launch import JobLaunch
from ..utilities import Utilities
from ..cli import CommandInvoker


@DeclarePlugin('slurm', 100)
class SlurmJobLaunch(JobLaunch):

    def __init__(self):
        self.util = Utilities()
        self.cmd_invoker = CommandInvoker()

    def remove_last_empty_line(self, str):
        index = str.rfind('\n')
        if index == -1 or index + 1 != len(str):
            return str
        return str[:index]

    def make_job_launch_cmd(self, job_script, node_count, nodes, output_file):
        cmd = ['sbatch', job_script]
        if node_count is not None:
            cmd.insert(1, '-N ' + node_count)
        if nodes is not None:
            cmd.insert(1, '-w ' + ','.join(nodes))
        if output_file is not None:
            cmd.insert(1, '-o ' + output_file)
            cmd.insert(1, '-e ' + output_file)
        return cmd

    def launch_batch_job(self, job_script,
                         node_count=None, nodes=None, output_file=None):
        if job_script is None:
            return 1, 'Job script is mandatory!'

        cmd = self.make_job_launch_cmd(job_script, node_count,
                                       nodes, output_file)
        result = self.util.execute_subprocess(cmd)
        if result.return_code != 0:
            return result.return_code, os.linesep + \
                   self.remove_last_empty_line(result.stderr.decode())
        job_id = result.stdout.decode().split()[3]
        return result.return_code, \
            'Job submitted successfully with id:' + job_id

    def append_options(self, cmd, job_id, state):
        if job_id is not None:
            cmd.append('--jobs=' + job_id)
        if state is not None:
            cmd.append('--state=' + state)

    def make_sacct_cmd(self, job_id, state):
        fields = '--format=User,JobID,NodeList,State,Start,Elapsed,ExitCode'
        cmd = ['sacct', fields]
        self.append_options(cmd, job_id, state)
        return cmd

    def make_squeue_cmd(self, job_id, state):
        cmd = ['squeue']
        self.append_options(cmd, job_id, state)
        return cmd

    def check_sacct_enabled(self):
        result = self.util.execute_subprocess(['sacct', '--help'])
        if result.return_code != 0:
            return False
        return True

    def check_job_metadata_common(self, cmd_maker, job_id, state, len_count):
        result = self.util.execute_subprocess(cmd_maker(job_id, state))
        if result.return_code != 0:
            return result.return_code, os.linesep + \
                   self.remove_last_empty_line(result.stderr.decode())
        result.stdout = self.remove_last_empty_line(result.stdout.decode())
        if len(result.stdout.split(os.linesep)) == len_count:
            return 1, 'No jobs found!'
        return result.return_code, os.linesep + result.stdout

    def check_job_metadata(self, job_id=None, state=None):
        if self.check_sacct_enabled():
            return self.check_job_metadata_common(self.make_sacct_cmd,
                                                  job_id, state, 2)
        self.cmd_invoker.logger.warning('SLURM accounting storage is disabled, '
                                        'looking for jobs in pending/running state')

        return self.check_job_metadata_common(self.make_squeue_cmd,
                                              job_id, state, 1)

    def cancel_job(self, job_id):
        if job_id is None:
            return 1, 'Job id is mandatory!'
        job_ret = self.check_job_metadata(job_id=job_id)
        if job_ret[0] != 0:
            return 1, 'No jobs found!'
        result = self.util.execute_subprocess(['scancel', job_id, '-v'])
        if result.return_code != 0:
            return result.return_code, os.linesep + \
                   self.remove_last_empty_line(result.stderr.decode())
        if 'error' in result.stderr.decode():
            return 1, os.linesep + self.remove_last_empty_line(result.stderr.decode())
        return result.return_code, 'Job has been cancelled successfully!'