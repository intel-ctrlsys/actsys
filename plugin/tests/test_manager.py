"""
Tests for the plugin manager.
"""
import unittest
from ctrl.plugin.manager import PLUGIN_METADATA_CLASS
from ctrl.plugin.manager import PLUGIN_FILE_EXTENSION
from ctrl.plugin.manager import PluginManager
from ctrl.plugin.manager import PluginMetadataInterface
import os
import shutil


class Instance1(object):
    """Test in module plugin."""
    def get_name(self):
        """Only API."""
        return "Testing...1...2...3..."


class Special1(object):
    """Test metadata"""
    def category(self):
        """Test category"""
        return "special"

    def name(self):
        """Test name"""
        return "provider1"

    def priority(self):
        """Test priority"""
        return 100

    def create_instance(self, options=None):
        """Test factory"""
        return Instance1()


class Special2(object):
    """Test metadata"""
    def __init__(self, category='special', name='provider2'):
        self.__category = category
        self.__name = name

    def category(self):
        """Test category"""
        return self.__category

    def name(self):
        """Test name"""
        return self.__name

    def priority(self):
        """Test priority"""
        return 100

    def create_instance(self, options=None):
        """Test factory"""
        return Instance1()


class Special3(object):
    """Test metadata"""
    def category(self):
        """Test category"""
        return "special"

    def name(self):
        """Test name"""
        return "provider2"

    def priority(self):
        """Test priority"""
        return 1

    def create_instance(self, options=None):
        """Test factory"""
        return Instance1()


class Special4(object):
    """Test metadata"""
    def category(self):
        """Test category"""
        return "special"

    def name(self):
        """Test name"""
        return "provider2"

    def priority(self):
        """Test priority"""
        return 1000

    def create_instance(self, options=None):
        """Test factory"""
        return Instance1()


class TestPluginManager(unittest.TestCase):
    """Test case for PluginManager class"""
    def setUp(self):
        """Common per test method startup."""
        self.__dir_name = 'test_plugins'
        self.__special = 'special_plugins'

        cwd = os.curdir
        dir_name = os.path.join(cwd, self.__dir_name)
        special_name = os.path.sep + os.path.join('tmp', self.__special)
        shutil.rmtree(dir_name, ignore_errors=True)
        os.mkdir(dir_name)
        shutil.rmtree(special_name, ignore_errors=True)
        os.mkdir(special_name)
        fd = open(os.path.join(dir_name, '__init__.py'), 'w')
        fd.close()
        index = 1
        for cat in range(1, 5):
            for n in range(1, 5):
                code = 'class %s:\n' % PLUGIN_METADATA_CLASS
                code += '    def category(self):\n'
                code += '        return "category%d"\n\n' % cat
                code += '    def name(self):\n'
                code += '        return "name%d"\n\n' % n
                code += '    def priority(self):\n'
                code += '        return %d\n\n' % (17 - index)
                code += '    def create_instance(self, options=None):\n'
                code += '        return TestInstance%d()\n\n\n' % index
                code += 'class TestInstance%d:\n' % index
                code += '    def get_name(self):\n'
                code += '        return "TestInstance%d"\n' % index
                raw_name = 'test%02d%s' % (index, PLUGIN_FILE_EXTENSION)
                fn = os.path.join(dir_name, raw_name)
                fd = open(fn, 'w')
                fd.write(code)
                fd.close()
                index += 1
        code = 'class %s:\n' % PLUGIN_METADATA_CLASS
        code += '    def category(self):\n'
        code += '        return "special_category"\n\n'
        code += '    def name(self):\n'
        code += '        return "special_name"\n\n'
        code += '    def priority(self):\n'
        code += '        return 101\n\n'
        code += '    def create_instance(self, options=None):\n'
        code += '        return SpecialInstance()\n\n\n'
        code += 'class SpecialInstance:\n'
        code += '    def get_name(self):\n'
        code += '        return "SpecialInstance"\n'
        raw_name = 'special%s' % PLUGIN_FILE_EXTENSION
        fn = os.path.join(special_name, raw_name)
        fd = open(fn, 'w')
        fd.write(code)
        fd.close()
        fd = open(os.path.sep + os.path.join(special_name, '__init__.py'), 'w')
        fd.close()

    def tearDown(self):
        """Common per test method cleanup."""
        cwd = os.curdir
        dir_name = os.path.join(cwd, self.__dir_name)
        special_name = os.path.sep + 'tmp'
        shutil.rmtree(dir_name, ignore_errors=True)
        shutil.rmtree(special_name, ignore_errors=True)

    def test_empty_ctor(self):
        """Test"""
        empty_manager = PluginManager()
        self.assertEquals(0, len(empty_manager.get_categories()))

    def test_folder_ctor_add_get(self):
        """Test"""
        manager = PluginManager(self.__dir_name)
        golden1 = ['category1', 'category2', 'category3', 'category4']
        cats = sorted(manager.get_categories())
        self.assertEqual(golden1, cats)
        self.assertEqual(4, len(manager.get_categories()))
        golden2 = ['name4', 'name3', 'name2', 'name1']
        for cat in cats:
            providers = manager.get_sorted_providers(cat)
            self.assertEqual(golden2, providers)

    def test_instances(self):
        """Test"""
        manager2 = PluginManager(self.__dir_name)
        for index in range(0, 16):
            cat = 'category%d' % ((index / 4) + 1)
            prov = 'name%d' % ((index % 4) + 1)
            obj = manager2.factory_create_instance(cat, prov)
            obj2 = manager2.factory_create_instance(cat, None)
            self.assertIsNotNone(obj2)
            golden = 'TestInstance%d' % (index + 1)
            self.assertEqual(golden, obj.get_name())
            self.assertIsNone(manager2.factory_create_instance(None, prov))
            self.assertIsNone(manager2.factory_create_instance('unknown', None))

    def test_multiple_folders(self):
        """Test"""
        special_name = os.path.sep + os.path.join('tmp', self.__special)
        manager3 = PluginManager(special_name)
        self.assertEqual(1, len(manager3.get_categories()))
        manager3.add_plugin_folder(self.__dir_name)
        self.assertEqual(5, len(manager3.get_categories()))
        manager3.add_plugin_folder(self.__dir_name)

    def test_in_code_additions(self):
        """Test"""
        manager4 = PluginManager(self.__dir_name)
        self.assertEqual(4, len(manager4.get_categories()))
        meta = Special1()
        manager4.add_provider(meta)
        self.assertEqual(5, len(manager4.get_categories()))
        inst = manager4.factory_create_instance(meta.category(), meta.name())
        self.assertEqual('Testing...1...2...3...', inst.get_name())
        with self.assertRaises(RuntimeWarning):
            meta2 = Special1()
            manager4.add_provider(meta2)
        self.assertEqual(5, len(manager4.get_categories()))
        meta3 = Special2()
        manager4.add_provider(meta3)
        meta3 = Special2(None)
        with self.assertRaises(RuntimeWarning):
            manager4.add_provider(meta3)
        meta3 = Special2('special', None)
        with self.assertRaises(RuntimeWarning):
            manager4.add_provider(meta3)
        self.assertEqual(5, len(manager4.get_categories()))
        inst3 = manager4.factory_create_instance(meta3.category(), meta3.name())
        self.assertEqual('Testing...1...2...3...', inst3.get_name())
        meta4 = Special3()
        manager4.add_provider(meta4)
        meta5 = Special4()
        manager4.add_provider(meta5)

    def test_safe_remove_file_positive(self):
        """Test"""
        fd = open('dummy_file.txt', 'w')
        fd.close()
        PluginManager.safe_remove_file('dummy_file.txt')
        self.assertFalse(os.path.isfile('dummy_file.txt'))

    def test_plugin_metadata_interface(self):
        """test the interface for complete coverage."""
        interface = PluginMetadataInterface()
        interface.category()
        interface.name()
        interface.priority()
        interface.create_instance()

if __name__ == '__main__':
    unittest.main()
