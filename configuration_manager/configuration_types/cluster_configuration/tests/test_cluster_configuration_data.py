#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Tests for ClusterConfigurationData Module """

from unittest import TestCase
from ctrl.configuration_manager.configuration_types.cluster_configuration.\
    cluster_configuration_data import ClusterConfigurationData
from ctrl.configuration_manager.objects.device import Device

class TestClusterConfigurationData(TestCase):
    """ Tests for ClusterConfigurationData Module """
    def setUp(self):
        """ Setup function"""
        self.container = ClusterConfigurationData(True)
        if self.container is not None:
            self.data = self.container.copy()

    def test___init__test_enabled(self):
        """ Test init function """
        self.assertIsNotNone(self.container)
        self.assertNotEqual(self.container, {})

    def test___init__test_disabled(self):
        """ Test init function """
        data_container = ClusterConfigurationData()
        data_container2 = ClusterConfigurationData(False)
        self.assertIsNotNone(data_container)
        self.assertIsNotNone(data_container2)
        self.assertEqual(data_container, data_container2)
        self.assertEqual(data_container2, {})

    def test__setitem__raises_TypeError(self):
        """ Test setitem function """
        self.assertRaises(TypeError, self.container.__setitem__, 'key', 'value')
        self.assertEqual(self.container, self.data)

    def test__setitem__raises_TypeError_invalid_Device(self):
        """ Test setitem function """
        self.assertRaises(TypeError, self.container.__setitem__, 'key',
                          Device({'device_types':'new_type',\
                                  'device_id':'myid', 'key':'value'}))
        self.assertEqual(self.container, self.data)

    def test__setitem__(self):
        """ Test setitem function """
        new_device = Device({'device_type':'new_type', 'device_id':'myid',\
                             'key':'value'})
        self.container[new_device.device_type] = new_device
        self.assertEqual(self.container['new_type']['myid'], new_device)

    def test_add_device_None(self):
        """ Test add_device function """
        self.assertFalse(self.container.add_device(None))
        self.assertEqual(self.container, self.data)

    def test_add_device_not_a_Device(self):
        """ Test add_device function """
        self.assertFalse(self.container.add_device(1))
        self.assertEqual(self.container, self.data)

    def test_add_device_empty_Device(self):
        """ Test add_device function """
        self.assertFalse(self.container.add_device(Device()))
        self.assertEqual(self.container, self.data)

    def test_add_device_no_device_type(self):
        """ Test add_device function """
        self.assertFalse(self.container.add_device(Device({'key':'value'})))
        self.assertEqual(self.container, self.data)

    def test_add_device_no_device_id(self):
        """ Test add_device function """
        new_device = Device({'device_type':'new_type', 'key':'value'})
        self.assertFalse(self.container.add_device(new_device))
        self.assertEqual(self.container, self.data)

    def test_add_device_new_device_type(self):
        """ Test add_device function """
        new_device = Device({'device_type':'new_type', 'device_id':'myid',\
                             'key':'value'})
        self.assertTrue(self.container.add_device(new_device))
        self.assertEqual(self.container['new_type']['myid'], new_device)

    def test_add_device_existing_device_type_new_device_id(self):
        """ Test add_device function """
        new_device = Device({'device_type':'node', 'device_id':'myid',\
                             'key':'value'})
        self.assertTrue(self.container.add_device(new_device))
        self.assertEqual(self.container['node']['myid'], new_device)

    def test_add_device_existing_device_type_existing_device_id(self):
        """ Test add_device function """
        new_device = Device({'device_type':'node', 'device_id':'master4',\
                             'key':'value'})
        self.assertTrue(self.container.add_device(new_device))
        self.assertEqual(self.container['node']['master4'], new_device)

    def test_search_device_no_type(self):
        """ Test serarch_device function """
        self.assertEqual(self.container.search_device('master4'), \
                         self.container['node']['master4'])

    def test_search_device_given_type(self):
        """ Test serarch_device function """
        self.assertEqual(self.container.search_device('master4', 'node'),\
                         self.container['node']['master4'])

    def test_search_device_invalid_id(self):
        """ Test serarch_device function """
        self.assertEqual(self.container.search_device('INVALID'), None)

    def test_search_device_invalid_type(self):
        """ Test serarch_device function """
        self.assertEqual(self.container.search_device('master4', 'INVALID'),\
                                                      None)

    def test_search_device_invalid_params(self):
        """ Test serarch_device function """
        self.assertEqual(self.container.search_device('INVALID', 'INVALID'),\
                                                      None)

