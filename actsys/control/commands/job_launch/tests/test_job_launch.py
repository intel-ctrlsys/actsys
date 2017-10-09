# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the Job launch Plugins.
"""
import unittest

from mock import MagicMock, patch

from .. import JobLaunch, JobCheck, JobCancel
from ....plugin.manager import PluginManager, PluginManagerException
from datastore import DataStore
from ...command import ConfigurationNeeded


class TestJobLaunch(unittest.TestCase):
    """Test case for the job launch classes."""

    @patch("datastore.DataStore", spec=DataStore)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.mock_plugin_manager = mock_plugin_manager
        self.setup_mock_config()
        self.job_mock = self.mock_plugin_manager.create_instance.return_value
        self.job_mock.launch_batch_job.return_value = (0, 'foo')
        self.job_mock.check_job_metadata.return_value = (0, 'foo')
        self.job_mock.cancel_job.return_value = (0, 'foo')
        self.config = {
                'device_name': 'mock-node',
                'configuration': self.configuration_manager,
                'plugin_manager': mock_plugin_manager,
                'logger': mock_logger,
            }
        self.job_launch = JobLaunch(**self.config)
        self.job_check = JobCheck(**self.config)
        self.job_cancel = JobCancel(**self.config)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        self.configuration_manager.get_device.return_value = {
            "ip_address": "192.168.1.1",
            "port": 22,
            "user": "user",
            "password": "pass",
            "device_type": "node",
            "service_list": []
        }

    def test_launch_execute(self):
        self.assertEqual(self.job_launch.execute().return_code, 0)

    def test_launch_execute_no_resource_controller(self):
        self.job_launch.resource_controller = None
        self.assertEqual(-1, self.job_launch.execute().return_code)

    def test_launch_execute_resource_manager_not_running(self):
        self.job_mock.check_resource_manager_running.return_value = False
        self.assertEqual(-2, self.job_launch.execute().return_code)

    def test_launch_invalid_resource_controller_configuration(self):
        self.mock_plugin_manager.create_instance.side_effect = \
            PluginManagerException("FooBar")
        try:
            self.job_launch.execute()
            self.fail("Should of thrown an exception")
        except ConfigurationNeeded as cn:
            self.assertTrue(str(cn).startswith("The configuration key"))

    def test_check_execute(self):
        self.assertEqual(self.job_check.execute().return_code, 0)

    def test_check_execute_no_resource_controller(self):
        self.job_check.resource_controller = None
        self.assertEqual(-1, self.job_check.execute().return_code)

    def test_cancel_execute(self):
        self.assertEqual(self.job_cancel.execute().return_code, 0)

    def test_cancel_execute_no_resource_controller(self):
        self.job_cancel.resource_controller = None
        self.assertEqual(-1, self.job_cancel.execute().return_code)

if __name__ == '__main__':
    unittest.main()
