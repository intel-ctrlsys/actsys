# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Job launch plugin manager
"""
from control.commands.command import CommandResult
from control.plugin import DeclarePlugin
from .job_launch_comm import JobLaunchCommand


@DeclarePlugin('job_launch', 100)
class JobLaunch(JobLaunchCommand):
    def __init__(self, device_name, configuration, plugin_manager, logger=None,
                 job_script=None, node_count=None, nodes=None,
                 output_file=None):
        JobLaunchCommand.__init__(self, device_name, configuration,
                                  plugin_manager, logger=logger,
                                  job_script=job_script,
                                  node_count=node_count, nodes=nodes,
                                  output_file=output_file)
        self.job_script = job_script
        self.node_count = node_count
        self.nodes = nodes
        self.output_file = output_file

    def execute(self):
        setup_result = self.setup()
        if setup_result is not None:
            return setup_result
        rc, message = self.job.launch_batch_job(self.job_script,
                          node_count=self.node_count, nodes=self.nodes,
                          output_file=self.output_file)
        return CommandResult(rc, message)
