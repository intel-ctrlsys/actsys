#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Tests for ClusterConfigurationParser Module """

from unittest import TestCase
from ..cluster_configuration_parser import ClusterConfigurationParser

class TestClusterConfigurationParser(TestCase):
    """ Tests for ClusterConfigurationData Module """
    def setUp(self):
        """ Setup function"""
        self.conf_file = \
            "control/configuration_manager/json_parser/tests/file.json"
        self.parser = ClusterConfigurationParser(self.conf_file)
        self.parser.parse()

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

