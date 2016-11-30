# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Configuration Manager Tests"""
import os
from unittest import TestCase
from ..configuration_manager import ConfigurationManager
from ..json_parser.json_parser import FileNotFound, NonParsableFile


def get_file_location(file_path):
    """ Gets the path to file to be used from this test directory"""
    prefix = ''
    if os.getcwd().endswith('tests'):
        prefix = '../../../'
    return "{0}{1}".format(prefix, file_path)

def read_file(file_path):
    """ Creates a configuration manager for the given file
    and returns its extractor """
    configuration_manager = ConfigurationManager(
        get_file_location(file_path))
    return  configuration_manager.get_extractor()


class TestConfigurationManager(TestCase):
    """ Configuration Manager Tests"""
    def setUp(self):
        self.conf_file = \
            'control/configuration_manager/json_parser/tests/file.json'
        ConfigurationManager._ConfigurationManager__configuration_objects = {}

    def test___init__(self):
        configuration_manager = \
            ConfigurationManager(get_file_location(self.conf_file))
        self.assertIsNotNone(configuration_manager)

    def test___init__file_not_found(self):
        self.assertRaises(FileNotFound, ConfigurationManager,
                          'unexistent_file.json')

    def test___init__file_not_parsable(self):
        file_name = \
           'control/configuration_manager/json_parser/tests/test_jsonParser.py'
        self.assertRaises(NonParsableFile, ConfigurationManager,
                          get_file_location(file_name))

    def test___init___two_instances(self):
        configuration_manager_1 = ConfigurationManager(
            get_file_location(self.conf_file))
        configuration_manager_2 = ConfigurationManager(
            get_file_location(self.conf_file))
        self.assertEqual(configuration_manager_1, configuration_manager_2,
                         "Two instances are not the same object")

    def test_get_extractor(self):
        self.assertIsNotNone(read_file(self.conf_file))

    def test_get_extractor_bad_type(self):
        configuration_manager = ConfigurationManager(
            get_file_location(self.conf_file))
        extractor = configuration_manager.get_extractor('FAKE_TYPE')
        self.assertIsNone(extractor)

    def test_version_json(self):
        self.assertIsNotNone(read_file(
            'control/configuration_manager/tests/version1.json'))

    def test_config_example(self):
        extractor = read_file('control/config-example.json')
        self.assertIsNotNone(extractor)
        self.assertEqual(4, len(extractor.get_devices_by_type('node')))
        self.assertEqual(4, len(extractor.get_devices_by_type('bmc')))
        self.assertEqual(2, len(extractor.get_devices_by_type('pdu')))
        self.assertEqual({}, extractor.get_devices_by_type('psu'))
        self.assertEqual(extractor.get_bmc('compute-29-bmc'),
                         extractor.get_node('compute-29').bmc)
        self.assertEqual(extractor.get_node('compute-29').pdu_list,
                         [('pdu-1', '5')])


