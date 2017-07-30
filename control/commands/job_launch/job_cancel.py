# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Job cancel plugin manager
"""
from control.commands.command import CommandResult
from control.plugin import DeclarePlugin
from .job_launch_comm import JobLaunchCommand


@DeclarePlugin('job_cancel', 100)
class JobCancel(JobLaunchCommand):
    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 job_id=None):
        JobLaunchCommand.__init__(self, device_name, configuration,
                                  plugin_manager, logger)
        self.job_id = job_id

    def execute(self):
        setup_result = self.setup()
        if setup_result is not None:
            return setup_result
        rc, message = self.job.cancel_job(self.job_id)
        return CommandResult(rc, message)
