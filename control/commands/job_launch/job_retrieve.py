# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Job retrieve plugin manager
"""
from control.commands.command import CommandResult
from control.plugin import DeclarePlugin
from .job_launch_comm import JobLaunchCommand


@DeclarePlugin('job_retrieve', 100)
class JobRetrieve(JobLaunchCommand):
    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 job_id=None, output_file=None):
        JobLaunchCommand.__init__(self, device_name, configuration,
                                  plugin_manager, logger=logger, job_id=job_id,
                                  output_file=output_file)
        self.job_id = job_id
        self.output_file = output_file

    def execute(self):
        setup_result = self.setup()
        if setup_result is not None:
            return setup_result
        rc, message = self.job.retrieve_job_result(
            self.job_id, output_file=self.output_file)
        return CommandResult(rc, message)
