#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Tests for ClusterConfiguration Module """

from unittest import TestCase
from ..cluster_configuration \
    import ClusterConfiguration, ClusterConfigurationExtractor
from ..cluster_configuration_data import ClusterConfigurationData
from ....tests.test_json_files import TestJsonFiles

class TestClusterConfiguration(TestCase):
    """ Tests for ClusterConfiguration """

    @classmethod
    def setUpClass(cls):
        """ Setup function for this class """
        cls.file_path = 'file.json'
        TestJsonFiles.write_file(cls.file_path)

    def setUp(self):
        """ Setup function """
        self.cconfig = ClusterConfiguration(TestClusterConfiguration.file_path)

    @classmethod
    def tearDownClass(cls):
        """ Teardown function for this class """
        TestJsonFiles.remove_file(cls.file_path)

    def test__init__(self):
        """ Test init function """
        self.assertIsNotNone(self.cconfig)
        self.assertEqual(TestClusterConfiguration.file_path,
                         self.cconfig.file_path)
        self.assertIsNone(self.cconfig.extractor)
        self.assertIsNone(self.cconfig.data)
        self.assertIsNone(self.cconfig.parser)

    def test_get_extractor(self):
        """ Test get_extractor function """
        self.assertEqual(self.cconfig.extractor, self.cconfig.get_extractor())

    def test_parse(self):
        """ Test parse function """
        self.assertTrue(self.cconfig.parse())
        self.assertIsNotNone(self.cconfig.data)
        self.assertIsNotNone(self.cconfig.extractor)

    def test_parse_negative(self):
        """ Test parse function """
        TestJsonFiles.write_file('bad_version.json')
        self.cconfig = ClusterConfiguration('bad_version.json')
        self.assertFalse(self.cconfig.parse())
        self.assertIsNone(self.cconfig.data)
        self.assertIsNone(self.cconfig.extractor)
        TestJsonFiles.remove_file('bad_version.json')


class TestClusterConfigurationExtractor(TestCase):
    """ Tests for ClusterConfigurationExtractor """
    def setUp(self):
        """ Setup function"""
        self.data = ClusterConfigurationData(True)
        self.extractor = ClusterConfigurationExtractor(self.data)

    def test__init__(self):
        """ Test init function """
        self.assertIsNotNone(self.extractor)
        self.assertEqual(self.data, self.extractor.data)

    def test__init__invalid_data(self):
        """ Test init function """
        self.assertRaises(TypeError, ClusterConfigurationExtractor,
                          'invalid_data')

    def test_get_device_types(self):
        """ Test get_device_types function """
        self.assertEqual(self.data.keys(), self.extractor.get_device_types())

    def test_get_devices_by_type(self):
        """ Test get_devices_by_type function """
        self.assertEqual(self.data[self.extractor.NODE_TAG], \
            self.extractor.get_devices_by_type(self.extractor.NODE_TAG))
        self.assertEqual(self.data[self.extractor.BMC_TAG], \
            self.extractor.get_devices_by_type(self.extractor.BMC_TAG))
        self.assertEqual(self.data[self.extractor.PSU_TAG], \
            self.extractor.get_devices_by_type(self.extractor.PSU_TAG))
        self.assertEqual(self.data[self.extractor.PDU_TAG], \
            self.extractor.get_devices_by_type(self.extractor.PDU_TAG))
        self.assertEqual(self.data[self.extractor.CONFIG_VARS_TAG], \
            self.extractor.get_devices_by_type(self.extractor.CONFIG_VARS_TAG))

    def test_get_devices_by_type_negative(self):
        """ Test get_devices_by_type function """
        self.assertEqual({}, self.extractor.get_devices_by_type('invalid'))

    def test_get_device(self):
        """ Test get_device function """
        self.assertEqual(self.data[self.extractor.NODE_TAG]['master4'],
                         self.extractor.get_device('master4'))
        self.assertEqual(self.data[self.extractor.BMC_TAG]['192.168.2.32'],
                         self.extractor.get_device('192.168.2.32'))
        self.assertEqual(self.data[self.extractor.PSU_TAG]['192.168.4.32'],
                         self.extractor.get_device('192.168.4.32'))
        self.assertEqual(self.data[self.extractor.PDU_TAG]['192.168.3.32'],
                         self.extractor.get_device('192.168.3.32'))
        self.assertEqual(self.data[self.extractor.CONFIG_VARS_TAG] \
            [self.extractor.CONFIG_VARS_TAG], \
            self.extractor.get_device(self.extractor.CONFIG_VARS_TAG))


    def test_get_device_negative(self):
        """ Test get_device function """
        self.assertIsNone(self.extractor.get_device('invalid'))

    def test_get_node(self):
        """ Test get_node function """
        self.assertEqual(self.data[self.extractor.NODE_TAG]['master4'],
                         self.extractor.get_node('master4'))
        self.assertIsNone(self.extractor.get_node('invalid'))

    def test_get_bmc(self):
        """ Test get_bmc function """
        self.assertEqual(self.data[self.extractor.BMC_TAG]['192.168.2.32'],
                         self.extractor.get_bmc('192.168.2.32'))
        self.assertIsNone(self.extractor.get_bmc('invalid'))

    def test_get_psu(self):
        """ Test get_psu function """
        self.assertEqual(self.data[self.extractor.PSU_TAG]['192.168.4.32'],
                         self.extractor.get_psu('192.168.4.32'))
        self.assertIsNone(self.extractor.get_psu('invalid'))

    def test_get_pdu(self):
        """ Test get_pdu function """
        self.assertEqual(self.data[self.extractor.PDU_TAG]['192.168.3.32'],
                         self.extractor.get_pdu('192.168.3.32'))
        self.assertIsNone(self.extractor.get_pdu('invalid'))

    def test_get_config_vars(self):
        """ Test get_config_vars function """
        self.assertEqual(self.data[self.extractor.CONFIG_VARS_TAG] \
            [self.extractor.CONFIG_VARS_TAG], self.extractor.get_config_vars())
