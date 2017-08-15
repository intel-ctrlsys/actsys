# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Job launch plugin common functionality
"""
from ..command import Command, CommandResult, ConfigurationNeeded


class JobLaunchCommand(Command):
    def __init__(self, device_name, configuration,
                 plugin_manager, logger=None, **kwargs):
        Command.__init__(self, 'UNDEF', configuration, plugin_manager,
                         logger, **kwargs)
        self.resource_controller = self.configuration.get_profile('compute_node')['resource_controller']
        self.job = None
        self.resource_manager = None

    def setup(self):
        if self.resource_controller is None:
            return CommandResult(-1, 'The resource manager for '
                                     'profile compute_node is not specified')
        try:
            self.job = self.plugin_manager.create_instance(
                'job_launch', self.resource_controller)
        except:
            raise ConfigurationNeeded('resource_controller',
                                      'profile: compute_node',
                                      self.plugin_manager.
                                      get_sorted_plugins_for_framework
                                      ("job_launch"))
        self.resource_manager = self.plugin_manager.create_instance('resource_control', self.resource_controller)
        if not self.resource_manager.check_resource_manager_running():
            return CommandResult(-2, "Resource manager is not running!")
        return None