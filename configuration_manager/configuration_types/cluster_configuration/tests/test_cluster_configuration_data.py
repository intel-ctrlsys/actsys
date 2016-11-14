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
        self.dc = ClusterConfigurationData(True)
        if self.dc is not None:
            self.data = self.dc.copy()

    def test___init__test_enabled(self):
        self.assertIsNotNone(self.dc)
        self.assertNotEqual(self.dc, {})

    def test___init__test_disabled(self):
        data_container = ClusterConfigurationData()
        data_container2 = ClusterConfigurationData(False)
        self.assertIsNotNone(data_container)
        self.assertIsNotNone(data_container2)
        self.assertEqual(data_container, data_container2)
        self.assertEqual(data_container2, {})

    def test__setitem__raises_TypeError(self):
        self.assertRaises(TypeError, self.dc.__setitem__, 'key', 'value')
        self.assertEqual(self.dc, self.data)

    def test__setitem__raises_TypeError_invalid_Device(self):
        self.assertRaises(TypeError, self.dc.__setitem__, 'key',
                          Device({'device_types':'new_type',\
                                  'device_id':'myid', 'key':'value'}))
        self.assertEqual(self.dc, self.data)

    def test__setitem__(self):
        new_device = Device({'device_type':'new_type', 'device_id':'myid',\
                             'key':'value'})
        self.dc[new_device.device_type] = new_device
        self.assertEqual(self.dc['new_type']['myid'], new_device)

    def test_add_device_None(self):
        self.assertFalse(self.dc.add_device(None))
        self.assertEqual(self.dc, self.data)

    def test_add_device_not_a_Device(self):
        self.assertFalse(self.dc.add_device(1))
        self.assertEqual(self.dc, self.data)

    def test_add_device_empty_Device(self):
        self.assertFalse(self.dc.add_device(Device()))
        self.assertEqual(self.dc, self.data)

    def test_add_device_no_device_type(self):
        self.assertFalse(self.dc.add_device(Device({'key':'value'})))
        self.assertEqual(self.dc, self.data)

    def test_add_device_no_device_id(self):
        new_device = Device({'device_type':'new_type', 'key':'value'})
        self.assertFalse(self.dc.add_device(new_device))
        self.assertEqual(self.dc, self.data)

    def test_add_device_new_device_type(self):
        new_device = Device({'device_type':'new_type', 'device_id':'myid',\
                             'key':'value'})
        self.assertTrue(self.dc.add_device(new_device))
        self.assertEqual(self.dc['new_type']['myid'], new_device)

    def test_add_device_existing_device_type_new_device_id(self):
        new_device = Device({'device_type':'NODE', 'device_id':'myid',\
                             'key':'value'})
        self.assertTrue(self.dc.add_device(new_device))
        self.assertEqual(self.dc['NODE']['myid'], new_device)

    def test_add_device_existing_device_type_existing_device_id(self):
        new_device = Device({'device_type':'NODE', 'device_id':'host1',\
                             'key':'value'})
        self.assertTrue(self.dc.add_device(new_device))
        self.assertEqual(self.dc['NODE']['host1'], new_device)

    def test_search_device_no_type(self):
        self.assertEqual(self.dc.search_device('host1'), \
                                               self.dc['NODE']['host1'])

    def test_search_device_given_type(self):
        self.assertEqual(self.dc.search_device('host1', 'NODE'),\
                                               self.dc['NODE']['host1'])

    def test_search_device_invalid_id(self):
        self.assertEqual(self.dc.search_device('INVALID'), None)

    def test_search_device_invalid_type(self):
        self.assertEqual(self.dc.search_device('host1', 'INVALID'), None)

    def test_search_device_invalid_params(self):
        self.assertEqual(self.dc.search_device('INVALID', 'INVALID'), None)

