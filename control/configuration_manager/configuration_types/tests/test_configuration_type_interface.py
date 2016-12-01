#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Tests for ConfigurationTypeInterface """

from unittest import TestCase
from ..configuration_type_interface \
    import ConfigurationTypeInterface

class ConfigurationTypeNotImplemented(
        ConfigurationTypeInterface):
    """ ConfigurationType Class without implementation
    for its abstract methods """

    def parse(self):
        """ Implements parse """
        return super(ConfigurationTypeNotImplemented,
                     self).parse()

    def get_extractor(self):
        """ Implements get_extractor """
        return super(ConfigurationTypeNotImplemented,
                     self).get_extractor()


class TestConfigurationTypeInterface(TestCase):
    """ Tests for ConfigurationType Interface """
    def setUp(self):
        """ Setup function"""
        self.file_path = 'file.json'
        self.cti = ConfigurationTypeNotImplemented(self.file_path)

    def test___init__(self):
        """ Test init function """
        self.assertIsNotNone(self.cti)
        self.assertEqual(self.file_path, self.cti.file_path)
        self.assertIsNone(self.cti.extractor)
        self.assertIsNone(self.cti.data)
        self.assertIsNone(self.cti.parser)

    def test_parse(self):
        """ Test parse function """
        self.assertRaises(NotImplementedError, self.cti.parse)

    def test_get_extractor(self):
        """ Test get_extractor function """
        self.assertRaises(NotImplementedError, self.cti.get_extractor)

