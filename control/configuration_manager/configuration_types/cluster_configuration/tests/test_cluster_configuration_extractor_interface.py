#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Tests for ClusterConfigurationExtractorInterface """

from unittest import TestCase
from ..cluster_configuration_extractor_interface \
    import ClusterConfigurationExtractorInterface

class ClusterConfigurationExtractorNotImplemented(
        ClusterConfigurationExtractorInterface):
    """ ClusterConfigurationExtractor Class without implementation
    for its abstract methods """

    def get_device(self, device):
        """ Implements get_device """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_device(device)
    def get_node(self, device):
        """ Implements get_node """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_node(device)
    def get_bmc(self, device):
        """ Implements get_bmc """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_bmc(device)
    def get_pdu(self, device):
        """ Implements get_pdu """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_pdu(device)
    def get_psu(self, device):
        """ Implements get_psu """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_psu(device)
    def get_config_vars(self):
        """ Implements get_config_vars """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_config_vars()
    def get_devices_by_type(self, device_type):
        """ Implements  get_devices_by_type """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_devices_by_type(device_type)
    def get_device_types(self):
        """ Implements get_device_types """
        return super(ClusterConfigurationExtractorNotImplemented,
                     self).get_device_types()


class TestClusterConfigurationExtractorInterface(TestCase):
    """ Tests for ClusterConfigurationExtractor Interface """
    def setUp(self):
        """ Setup function"""
        self.cce = ClusterConfigurationExtractorNotImplemented()

    def test___init__(self):
        """ Test init function """
        self.assertIsNotNone(self.cce)

    def test_get_device(self):
        """ Test  function """
        self.assertRaises(NotImplementedError, self.cce.get_device, 'dev')

    def test_get_bmc(self):
        """ Test get_bmc function """
        self.assertRaises(NotImplementedError, self.cce.get_bmc, 'dev')

    def test_get_pdu(self):
        """ Test get_pdu function """
        self.assertRaises(NotImplementedError, self.cce.get_pdu, 'dev')

    def test_get_psu(self):
        """ Test get_psu function """
        self.assertRaises(NotImplementedError, self.cce.get_psu, 'dev')

    def test_get_config_vars(self):
        """ Test get_config_vars function """
        self.assertRaises(NotImplementedError, self.cce.get_config_vars)

    def test_get_devices_by_type(self):
        """ Test get_devices_by_type function """
        self.assertRaises(NotImplementedError, self.cce.get_devices_by_type,
                          'dev')

    def test_get_device_types(self):
        """ Test  get_device_types function """
        self.assertRaises(NotImplementedError, self.cce.get_device_types)

    def test_get_node(self):
        """ Test get_node function """
        self.assertRaises(NotImplementedError, self.cce.get_node, 'dev')

