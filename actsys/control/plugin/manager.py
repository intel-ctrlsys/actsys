# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This class defines how plugins are created from a folder.
"""

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

    # TODO: framework => adapter and plugin => provider

    @classmethod
    def _make_key(cls, framework_name, plugin_name):
        """Create a key from the category and provider name."""
        if framework_name is None or plugin_name is None:
            err = 'Neither the "framework_name" or the "plugin_name" are allowed to be "None"!'
            raise PluginManagerException(err)
        return '{}{}{}'.format(framework_name, PLUGIN_KEY_SEPARATOR,
                               plugin_name)

    @classmethod
    def _split_key(cls, key):
        """Split the key into category and provider name."""
        return key.split(PLUGIN_KEY_SEPARATOR)

    def __init__(self):
        """Constructor that may add the first folder of plugins."""
        self.__plugin_files = list()
        self.__plugin_frameworks = dict()

    def register_plugin_class(self, cls):
        """Add this provider to the list."""
        key = PluginManager._make_key(cls.FRAMEWORK_NAME,
                                      cls.PLUGIN_NAME)
        if key in list(self.__plugin_frameworks.keys()):
            if cls.PLUGIN_PRIORITY == self.__plugin_frameworks[key].PLUGIN_PRIORITY:
                err = 'There is a collision of framework plugin and priority. The same named plugin in a framework ' \
                      'cannot have equal priority.'
                raise PluginManagerException(err)
            elif cls.PLUGIN_PRIORITY < self.__plugin_frameworks[key].PLUGIN_PRIORITY:
                self.__plugin_frameworks[key] = cls
        else:
            self.__plugin_frameworks[key] = cls

    def get_frameworks(self):
        """Retrieve the list of unique provider frameworks."""
        frameworks = list()
        for key in list(self.__plugin_frameworks.keys()):
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
        for entry in list(self.__plugin_frameworks.keys()):
            keys.append(entry)
        return keys

    def get_sorted_plugins_for_framework(self, framework):
        """Retrieve the list of plugins for a specific framework."""
        providers = list()
        for key in list(self.__plugin_frameworks.keys()):
            stored_framework, name = PluginManager._split_key(key)
            if framework == stored_framework:
                providers.append((self.__plugin_frameworks[key].
                                  PLUGIN_PRIORITY, name))
        providers.sort()
        provider_list = []
        for item in providers:
            provider_list.append(item[1])
        return provider_list

    def create_instance(self, framework_name, plugin_name, **kwargs):
        """Create a named (or default) provider in the specified category."""
        if framework_name is None or plugin_name is None:
            raise PluginManagerException('Cannot create a plugin where the framework_name or plugin_name is None.')
        key = PluginManager._make_key(framework_name, plugin_name)
        try:
            return self.__plugin_frameworks[key](**kwargs)
        except KeyError:
            raise PluginManagerException('Plugin "{}" was not found for framework "{}"'.
                                         format(plugin_name, framework_name))
