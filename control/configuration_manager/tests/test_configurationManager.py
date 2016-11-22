# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
from unittest import TestCase

from ..configuration_manager import ConfigurationManager


class TestConfigurationManager(TestCase):
    def setUp(self):
        self.conf_file = \
            'control/configuration_manager/json_parser/tests/file.json'

    def test___init__(self):
        configuration_manager = ConfigurationManager(self.conf_file)
        self.assertIsNotNone(configuration_manager)

    def test___init___two_instances(self):
        configuration_manager_1 = ConfigurationManager(self.conf_file)
        configuration_manager_2 = ConfigurationManager(self.conf_file)
        self.assertEqual(configuration_manager_1, configuration_manager_2,
                         "Two instances are not the same object")

    def test_get_extractor(self):
        configuration_manager = ConfigurationManager(self.conf_file)
        extractor = configuration_manager.get_extractor()
        self.assertIsNotNone(extractor)

    def test_get_extractor_negative(self):
        configuration_manager = ConfigurationManager(self.conf_file)
        extractor = configuration_manager.get_extractor('FAKE_TYPE')
        self.assertIsNone(extractor)
