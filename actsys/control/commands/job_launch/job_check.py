# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Job check metadata plugin manager
"""
from control.commands.command import CommandResult
from control.plugin import DeclarePlugin
from .job_launch_comm import JobLaunchCommand


@DeclarePlugin('job_check', 100)
class JobCheck(JobLaunchCommand):
    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 job_id=None, state=None):
        JobLaunchCommand.__init__(self, device_name, configuration,
                                  plugin_manager, logger, job_id=job_id,
                                  state=state)
        self.job_id = job_id
        self.state = state

    def execute(self):
        setup_result = self.setup()
        if setup_result is not None:
            return setup_result
        rc, message = self.job.check_job_metadata(
            job_id=self.job_id, state=self.state)
        return CommandResult(rc, message)
