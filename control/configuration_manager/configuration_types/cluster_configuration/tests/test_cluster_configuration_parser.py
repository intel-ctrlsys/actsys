#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Tests for ClusterConfigurationParser Module """

from unittest import TestCase
from ..cluster_configuration_parser \
    import ClusterConfigurationParser, expand_group
from ....tests.test_json_files import TestJsonFiles


class TestClusterConfigurationParser(TestCase):
    """ Tests for ClusterConfigurationData Module """

    def setUp(self):
        """ Setup function"""
        self.conf_file = 'file.json'
        TestJsonFiles.write_file(self.conf_file)
        self.parser = ClusterConfigurationParser(self.conf_file)
        self.parser.parse()
        TestJsonFiles.remove_file(self.conf_file)

    def test_expand_goup_different_len(self):
        group = {'device_id':'compute-[1:29-32]', 'device_type':'node',
                 'someattr':'hello', 'ip_address': '192.168.2.[1:29-32]',
                 'bmc':'bmc[1:1-3]'}
        expected = [{'device_id':'compute-29', 'device_type':'node',
                     'someattr':'hello', 'ip_address': '192.168.2.29',
                     'bmc':'bmc1'},
                    {'device_id':'compute-30', 'device_type':'node',
                     'someattr':'hello', 'ip_address': '192.168.2.30',
                     'bmc':'bmc2'},
                    {'device_id':'compute-31', 'device_type':'node',
                     'someattr':'hello', 'ip_address': '192.168.2.31',
                     'bmc':'bmc3'}]
        self.assertEqual(expand_group(group), expected)

    def test_expand_goup_(self):
        group = {'device_id':'compute-[1:29-32]', 'device_type':'node',
                 'someattr':'hello', 'ip_address': '192.168.2.[1:29-32]',
                 'hostname':'compute-[1:29-32]'}
        expected = [{'device_id':'compute-29', 'device_type':'node',
                     'someattr':'hello', 'ip_address': '192.168.2.29',
                     'hostname':'compute-29'},
                    {'device_id':'compute-30', 'device_type':'node',
                     'someattr':'hello', 'ip_address': '192.168.2.30',
                     'hostname':'compute-30'},
                    {'device_id':'compute-31', 'device_type':'node',
                     'someattr':'hello', 'ip_address': '192.168.2.31',
                     'hostname':'compute-31'},
                    {'device_id':'compute-32', 'device_type':'node',
                     'someattr':'hello', 'ip_address': '192.168.2.32',
                     'hostname':'compute-32'}]
        self.assertEqual(expand_group(group), expected)

    def test__set_node_relationships__(self):
        self.assertEquals(self.parser.parsed_data['node']['master4'].bmc,
                          self.parser.parsed_data['bmc']['192.168.2.32'])
        self.assertEquals(self.parser.parsed_data['node']['master5'].bmc,
                          self.parser.parsed_data['bmc']['bmc2'])

    def test__set_pdu_relationships__(self):
        self.assertEquals(
            self.parser.parsed_data['node']['master4'].pdu_list,
            [('192.168.3.32', '3')])
        self.assertEquals(
            self.parser.parsed_data['node']['master5'].pdu_list,
            [('pdu2', '3')])
        self.assertEquals(
            self.parser.parsed_data['bmc']['bmc2'].pdu_list,
            [('pdu2', '0')])
        self.assertEquals(
            self.parser.parsed_data['psu']['192.168.4.32'].pdu_list,
            [('192.168.3.32', '0')])
        self.assertEquals(
            self.parser.parsed_data['bmc']['192.168.2.32'].pdu_list, None)

    def test__set_psu_relationships__(self):
        self.assertEquals(self.parser.parsed_data['node']['master4'].psu_list,
                          [('192.168.4.32', '1')])
        self.assertEquals(self.parser.parsed_data['node']['master5'].psu_list,
                          [('192.168.4.32', '0')])
        self.assertEquals(self.parser.parsed_data['bmc']['bmc2'].psu_list,
                          None)
        self.assertEquals(
            self.parser.parsed_data['pdu']['192.168.3.32'].psu_list, None)

    def test_is_valid_hostname(self):
        valid_strings = ['a',
                         'ab',
                         '0a',
                         '00a',
                         '00a0-2-a',
                         'qwww',
                         'wWw',
                         'my-www',
                         '3www',
                         'host-5512']

        not_valid_strings = ['cosa_sad',
                             'my www',
                             'mu-',
                             'mu_',
                             'my_www',
                             '-www',
                             '5512',
                             '@www',
                             'something.some.othersome.com']

        for test_string in valid_strings:
            self.assertTrue(self.parser.__is_valid_hostname__(test_string),
                            'True expected for {0}'.format(test_string))
        for test_string in not_valid_strings:
            self.assertFalse(self.parser.__is_valid_hostname__(test_string),
                             'False expected for {0}'.format(test_string))

    def test_is_valid_ip(self):
        valid_strings = ['0.0.0.0',
                         '192.165.4.8',
                         '255.255.255.255']

        not_valid_strings = ['-1.25.65.45',
                             '192.168.1.2.5',
                             '256.168.1.1',
                             '192.256.4.8',
                             '192.165.256.8',
                             '192.165.4.256',
                             '1922.165.4.250'
                             '192.165.4.1111'
                             '']

        for test_string in valid_strings:
            self.assertTrue(self.parser.__is_valid_ip_addr__(test_string),
                            'True expected for {0}'.format(test_string))

