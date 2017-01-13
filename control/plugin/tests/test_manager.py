# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the plugin manager.
"""
from __future__ import print_function
import unittest
from ...plugin.manager import PluginManager, DeclarePlugin, DeclareFramework
import os


@DeclareFramework('framework1')
class ExampleFramework(object):
    def __init__(self, options=None):
        pass


@DeclarePlugin('plugin1', 100)
class ExamplePlugin1(ExampleFramework):
    pass


@DeclarePlugin('plugin2', 100)
class ExamplePlugin2(ExampleFramework):
    pass


@DeclarePlugin('plugin3', 100)
class ExamplePlugin3(ExampleFramework):
    pass


class TestPluginManager(unittest.TestCase):
    """Test case for PluginManager class"""
    def setUp(self):
        """Common per test method startup."""

    def tearDown(self):
        """Common per test method cleanup."""

    def test_empty_ctor(self):
        """Test"""
        empty_manager = PluginManager()
        self.assertEquals(0, len(empty_manager.get_frameworks()))

    @unittest.skip("Not yet working")
    def test_folder_ctor_add_get(self):
        """Test"""
        print (os.path.dirname(__file__))
        manager = PluginManager(os.path.dirname(__file__))
        print (manager.get_registered_plugins())
        self.assertGreater(len(manager.get_frameworks()), 0)
        self.assertGreater(len(manager.get_registered_plugins()), 0)

    def test_instances(self):
        """Test"""
        print (os.curdir)
        manager2 = PluginManager()
        manager2.register_plugin_class(ExamplePlugin1)
        manager2.register_plugin_class(ExamplePlugin2)
        self.assertEqual(2, len(manager2.get_registered_plugins()))
        manager2.register_plugin_class(ExamplePlugin3)
        self.assertEqual(3, len(manager2.get_registered_plugins()))

        inst = manager2.create_instance('framework1', 'plugin1')
        self.assertIsNotNone(inst)
        inst = manager2.create_instance('framework1', 'plugin2')
        self.assertIsNotNone(inst)
        inst = manager2.create_instance('framework1', 'plugin3')
        self.assertIsNotNone(inst)

    def test_in_code_additions(self):
        """Test"""
        manager4 = PluginManager()
        manager4.register_plugin_class(ExamplePlugin1)
        manager4.register_plugin_class(ExamplePlugin2)
        self.assertEqual(2, len(manager4.get_registered_plugins()))
        manager4.register_plugin_class(ExamplePlugin3)
        self.assertEqual(3, len(manager4.get_registered_plugins()))

        # Test A framework can be created
        inst = manager4.create_instance('framework1', 'plugin1')
        self.assertIsNotNone(inst)

        # Test for duplicate registration?
        with self.assertRaises(RuntimeWarning):
            manager4.register_plugin_class(ExamplePlugin1)

        self.assertEqual(3, len(manager4.get_registered_plugins()))

if __name__ == '__main__':
    unittest.main()
