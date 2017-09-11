# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Provides the PluginTools class, which is used for loading modules and
instantiating classes therein, from their names
"""

import importlib
from sys import modules


class PluginTools(object):
    """Provides a few functions supporting the use of plugin classes"""

    @staticmethod
    def instantiate(full_name, *args):
        cls = PluginTools.__get_plugin_class(full_name)
        obj = cls(*args)
        PluginTools.__check_plugin_config(obj)
        return obj

    @staticmethod
    def __check_plugin_config(obj):
        if not hasattr(obj, 'config') or not isinstance(obj.config, dict):
            raise AttributeError('plugin missing config dictionary')

    @staticmethod
    def __get_plugin_class(full_name):
        name_pieces = str(full_name).split('.')
        module_name = '.'.join(name_pieces[:-1])
        module = PluginTools.__get_module(module_name)
        class_name = name_pieces[-1]
        return getattr(module, class_name)

    @staticmethod
    def __get_module(module_name):
        if module_name not in modules:
            importlib.import_module(module_name)
        return modules[module_name]
