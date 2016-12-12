# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Configuration Manager Tests"""
import unittest
from ..configuration_manager import ConfigurationManager
from ..json_parser.json_parser import FileNotFound, NonParsableFile
from .test_json_files import TestJsonFiles


def read_file(file_path):
    """ Creates a configuration manager for the given file
    and returns its extractor """
    TestJsonFiles.write_file(file_path)
    configuration_manager = ConfigurationManager(file_path)
    TestJsonFiles.remove_file(file_path)
    return configuration_manager.get_extractor()


class TestConfigurationManager(unittest.TestCase):
    """ Configuration Manager Tests"""

    def setUp(self):
        self.conf_file = 'file.json'
        ConfigurationManager._ConfigurationManager__configuration_objects = {}

    def test___init__(self):
        TestJsonFiles.write_file(self.conf_file)
        configuration_manager = ConfigurationManager(self.conf_file)
        TestJsonFiles.remove_file(self.conf_file)
        self.assertIsNotNone(configuration_manager)

    def test___init__file_not_found(self):
        self.assertRaises(FileNotFound, ConfigurationManager,
                          'unexistent_file.json')

    def test___init__file_not_parsable(self):
        TestJsonFiles.write_file('non_parsable.json')
        self.assertRaises(NonParsableFile, ConfigurationManager, 'non_parsable.json')
        TestJsonFiles.remove_file('non_parsable.json')

    def test___init___two_instances(self):
        TestJsonFiles.write_file(self.conf_file)
        configuration_manager_1 = ConfigurationManager(self.conf_file)
        configuration_manager_2 = ConfigurationManager(self.conf_file)
        TestJsonFiles.remove_file(self.conf_file)
        self.assertEqual(configuration_manager_1, configuration_manager_2,
                         "Two instances are not the same object")

    def test_get_extractor(self):
        self.assertIsNotNone(read_file(self.conf_file))

    def test_get_extractor_bad_type(self):
        TestJsonFiles.write_file(self.conf_file)
        configuration_manager = ConfigurationManager(self.conf_file)
        TestJsonFiles.remove_file(self.conf_file)
        extractor = configuration_manager.get_extractor('FAKE_TYPE')
        self.assertIsNone(extractor)

    def test_version_json(self):
        self.assertIsNotNone(read_file('version1.json'))

    def test_bad_version_json(self):
        self.assertIsNone(read_file('bad_version.json'))

    def test_config_example(self):
        extractor = read_file('config-example.json')
        self.assertIsNotNone(extractor)
        self.assertEqual(4, len(extractor.get_devices_by_type('node')))
        self.assertEqual(4, len(extractor.get_devices_by_type('bmc')))
        self.assertEqual(2, len(extractor.get_devices_by_type('pdu')))
        self.assertEqual({}, extractor.get_devices_by_type('psu'))
        self.assertEqual(extractor.get_bmc('compute-29-bmc'),
                         extractor.get_node('compute-29').bmc)
        self.assertEqual(extractor.get_node('compute-29').pdu_list,
                         [('pdu-1', '5')])

    def test_deepcopy(self):
        extractor = read_file(self.conf_file)
        self.assertIsNotNone(extractor)

        dev = extractor.get_node('master4')
        dev.hostname = 'fake'
        self.assertNotEqual('fake', dev.hostname)
        self.assertNotEqual('fake', extractor.get_device('master4').hostname)

        dev.pdu_list.append('fake')
        self.assertNotEqual(dev.pdu_list,
                            extractor.get_node('master4').pdu_list)

        dev.rad.username = 'fake'
        self.assertEqual('fake', dev.rad.username)
        self.assertNotEqual(dev.rad, extractor.get_node('master4').rad)

        dev = extractor.get_config_vars()
        dev.log_file = {}
        self.assertNotEqual({}, dev.log_file)
        dev.log_file['fake'] = 'fake'
        self.assertIsNone(extractor.get_config_vars().log_file.get('fake'))

    def test_empty_values(self):
        extractor = read_file('version1.json')
        self.assertIsNotNone(extractor)
        self.assertEqual(0, extractor.get_node('master4').zero_field)
        self.assertEqual('', extractor.get_node('master4').empty_string)

    def test_unexistent_attribute(self):
        extractor = read_file('version1.json')
        self.assertIsNotNone(extractor)
        self.assertEqual(None, extractor.get_node('master4').unexistent_attribute)

    def test_unexistent_device(self):
        extractor = read_file('version1.json')
        self.assertIsNotNone(extractor)
        try:
            extractor.get_device('unexistent_node').any_attribute
        except AttributeError as aee:
            print aee
        else:
            self.fail()
