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
            cmd.insert(1, '-w ' + nodes)
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
                   self.remove_last_empty_line(result.stderr)
        job_id = result.stdout.split()[3]
        return result.return_code, \
            'Job submitted successfully with id:' + job_id

    def append_options(self, cmd, job_id, state):
        if job_id is not None:
            cmd.append('--jobs=' + job_id)
        if state is not None:
            cmd.append('--state=' + state)

    def make_sacct_cmd(self, job_id, state):
        fields = '--format=User,JobID,NodeList,State,Start,Elapsed,ExitCode'
        cmd = ['sacct', '--format=' + fields]
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
                   self.remove_last_empty_line(result.stderr)
        result.stdout = self.remove_last_empty_line(result.stdout)
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

    def find_file(self, job_id, output_file):
        file_name = output_file
        if output_file is None:
            file_name = 'slurm-' + job_id + '.out'
        result = self.util.execute_subprocess(['find', '/', '-name', file_name])
        if '' == result.stdout:
            return None
        return result.stdout.split(os.linesep)[0]

    def retrieve_job_result(self, job_id, output_file=None):
        if job_id is None:
            return 1, 'Job ID is mandatory'
        file_to_read = self.find_file(job_id, output_file)
        if file_to_read is None:
            return 1, 'Job output file does not exist!'
        ret = self.util.execute_subprocess(['cat', file_to_read])
        if ret.return_code != 0:
            return ret.return_code, ret.stderr
        return ret.return_code, ret.stdout

    def cancel_job(self, job_id):
        if job_id is None:
            return 1, 'Job id is mandatory!'
        result = self.util.execute_subprocess(['scancel', job_id, '-v'])
        if result.return_code != 0:
            return result.return_code, os.linesep + \
                   self.remove_last_empty_line(result.stderr)
        if 'error' in result.stderr:
            return 1, os.linesep + self.remove_last_empty_line(result.stderr)
        if 'scancel: Cray node' in  result.stderr:
            return 1, 'Invalid job ' + job_id
        return result.return_code, 'Job has been cancelled successfully!'