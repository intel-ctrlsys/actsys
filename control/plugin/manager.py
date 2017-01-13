# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This class defines how plugins are created from a folder.
"""
from __future__ import print_function
import imp
import os
import os.path
import inspect


PLUGIN_FILE_EXTENSION = '.py'
PLUGIN_KEY_SEPARATOR = '.'


class PluginManagerException(RuntimeWarning):
    """Specific exception class for the PluginManager class."""
    def __init__(self, message):
        super(RuntimeWarning, self).__init__(message)


class DeclarePlugin(object):
    """Decorator for Plugins"""
    def __init__(self, name, priority):
        self._name = name
        self._priority = priority

    def __call__(self, cls):
        """Decorator for plugins callable object"""
        class _Plugin(cls):
            PLUGIN_NAME = self._name
            PLUGIN_PRIORITY = self._priority

        return _Plugin


class DeclareFramework(object):
    """Decorator for Frameworks"""
    def __init__(self, name):
        self._name = name

    def __call__(self, cls):
        """Decorator for frameworks callable object"""
        class _Framework(cls):
            FRAMEWORK_NAME = self._name

        return _Framework


class PluginManager(object):
    """This class defines how plugins are created from a folder. """
    @classmethod
    def _safe_remove_file(cls, filename):
        """Remove a filename suppressing obvious exceptions."""
        if os.path.isfile(filename):
            os.remove(filename)

    @classmethod
    def _make_key(cls, framework_name, plugin_name):
        """Create a key from the category and provider name."""
        if framework_name is None or plugin_name is None:
            err = 'Neither the "framework_name" or the "plugin_name" are '\
                  'allowed to be "None"!'
            raise PluginManagerException(err)
        return '{}{}{}'.format(framework_name, PLUGIN_KEY_SEPARATOR,
                               plugin_name)

    @classmethod
    def _split_key(cls, key):
        """Split the key into category and provider name."""
        return key.split(PLUGIN_KEY_SEPARATOR)

    @classmethod
    def _walker_callback(cls, self, folder, files):
        for filename in files:
            parts = os.path.splitext(filename)
            if parts[1] == PLUGIN_FILE_EXTENSION and not \
                    parts[0] == '__init__' and not \
                    parts[0].startswith('test_'):
                full = os.path.join(folder, filename)
                self._add_plugin(full)

    def __init__(self, plugin_folder=None):
        """Constructor that may add the first folder of plugins."""
        self.__plugin_files = list()
        self.__plugin_frameworks = dict()
        if plugin_folder is not None:
            self.add_plugin_folder(plugin_folder)

    def add_plugin_folder(self, plugin_folder):
        """Add a folder of plugins to the manager."""
        os.walk(plugin_folder, PluginManager._walker_callback, self)

    def register_plugin_class(self, cls):
        """Add this provider to the list."""
        key = PluginManager._make_key(cls.FRAMEWORK_NAME,
                                      cls.PLUGIN_NAME)
        if key in self.__plugin_frameworks.keys():
            if cls.PLUGIN_PRIORITY == self.__plugin_frameworks[key].\
                    PLUGIN_PRIORITY:
                err = 'There is a collision of framework plugin and ' \
                      'priority. The same named plugin in a framework ' \
                      'cannot have equal priority.'
                raise PluginManagerException(err)
            elif cls.PLUGIN_PRIORITY < self.__plugin_frameworks[key].\
                    PLUGIN_PRIORITY:
                self.__plugin_frameworks[key] = cls
        else:
            self.__plugin_frameworks[key] = cls

    def get_frameworks(self):
        """Retrieve the list of unique provider frameworks."""
        frameworks = list()
        for key in self.__plugin_frameworks.keys():
            framework = PluginManager._split_key(key)[0]
            if framework not in frameworks:
                frameworks.append(framework)
        return frameworks

    def get_registered_plugins(self):
        """
        Returns the list of plugins (framework_name.plugin_name) registered
        in the manager.
        """
        keys = list()
        for entry in self.__plugin_frameworks.keys():
            keys.append(entry)
        return keys

    def get_sorted_plugins_for_framework(self, category):
        """Retrieve the list of plugins for a specific framework."""
        providers = list()
        for key in self.__plugin_frameworks.keys():
            stored_category, name = PluginManager._split_key(key)
            if category == stored_category:
                providers.append((self.__plugin_frameworks[key].
                                  PLUGIN_PRIORITY, name))
        providers.sort()
        provider_list = []
        for item in providers:
            provider_list.append(item[1])
        return provider_list

    def create_instance(self, framework_name, plugin_name=None, options=None):
        """Create a named (or default) provider in the specified category."""
        if framework_name is None:
            return None
        if plugin_name is None:
            frameworks = self.get_sorted_plugins_for_framework(framework_name)
            if frameworks is not None and len(frameworks) > 0:
                plugin_name = frameworks[0]
        if plugin_name is None or framework_name is None:
            return None
        key = PluginManager._make_key(framework_name, plugin_name)
        try:
            return self.__plugin_frameworks[key](options)
        except KeyError:
            raise PluginManagerException('Plugin "{}" was not found for '
                                         'framework "{}"'.
                                         format(plugin_name, framework_name))

    def _add_plugin(self, fullname):
        """Add the plugin to the dictionary."""
        if fullname not in self.__plugin_files:
            if self._load_metadata(fullname):
                self.__plugin_files.append(fullname)

    def _load_metadata(self, plugin_filename):
        """Load the plugin dynamically."""
        path_name, base_filename = os.path.split(plugin_filename)
        module_name = os.path.splitext(base_filename)[0]
        compiled = os.path.join(path_name, "%s.pyc" % module_name)
        PluginManager._safe_remove_file(compiled)
        module = imp.load_source(module_name, plugin_filename)
        result = False
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if hasattr(cls, 'PLUGIN_NAME') and \
                    hasattr(cls, 'PLUGIN_PRIORITY') and \
                    hasattr(cls, 'FRAMEWORK_NAME'):
                init = getattr(cls, '__init__', None)
                if init is not None:
                    arg_count = len(inspect.getargspec(init)[0])
                    if arg_count == 2 and \
                            inspect.getargspec(init)[0][0] == 'self':
                        self.register_plugin_class(cls)
                        result = True
        return result
