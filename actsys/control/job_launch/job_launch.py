# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Interface for all job launch plugins.
"""
from abc import ABCMeta, abstractmethod
from ..plugin import DeclareFramework


"""Interface for job launch classes."""


@DeclareFramework('job_launch')
class JobLaunch(object, metaclass=ABCMeta):
    @abstractmethod
    def launch_batch_job(self, job_script,
                         node_count=None, nodes=None, output_file=None):
        """launch a batch job specified in a script
        :param job_script: script that describes a job to be launched
        :param node_count: number of nodes required to run a job
        :param nodes: the nodes expected to be allocated to a job
        :param output_file: the output file where to put the result
        :return: A job id associated with the job to be launched
        """
        pass

    @abstractmethod
    def check_job_metadata(self, job_id=None, state=None):
        """check details of job
        :param job_id: which job to be checked
        :param state: check metadata of all jobs with certain state
        :return: job details (e.g. state (pending, running, completed),
                              nodelist, output file)
        """
        pass

    @abstractmethod
    def retrieve_job_result(self, job_id, output_file=None):
        """retrieve the result after a job is done
        :param job_id: which job to retrieve result
        :param output_file: from which output file to retrieve result
        :return: result after a job is done
        """
        pass

    @abstractmethod
    def cancel_job(self, job_id):
        """cancel a job
        :param job_id: which job to cancel
        :return: succeeded or not in canceling a job
        """
        pass
