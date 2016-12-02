# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
from unittest import TestCase
from ..configuration_manager_item import ConfigurationManagerItem


class TestConfigurationManagerItem(TestCase):
    def test___add_attribute__(self):
        item = ConfigurationManagerItem()
        item.__add_attribute__('test_attribute', 'test_value')
        self.assertEqual(['test_attribute'], item.get_attribute_list())
        self.assertEqual('''{'test_attribute': 'test_value'}''', item.__repr__())

    def test___eq__(self):
        item1 = ConfigurationManagerItem({'test_attribute': 'test_value'})
        item2 = ConfigurationManagerItem({'test_attribute': 'test_value'})
        self.assertEqual(item1, item2)
        self.assertFalse(item1 == 'different_object')

    def test___ne__(self):
        item1 = ConfigurationManagerItem({'test_attribute': 'test_value'})
        item2 = ConfigurationManagerItem({'test_attribute': 'another_test_value'})
        self.assertNotEqual(item1, item2)
        self.assertTrue(item1 <> 'different_object')
