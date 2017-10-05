# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Provides the Plugin class, used as a wrapper for user modules providing
REST resources.
"""

import importlib
from sys import modules

from oobrestserver.GlobTools import GlobTools


class Plugin(object):
    """Provides a few functions supporting the use of plugin classes"""

    @staticmethod
    def plugin(description):
        args = description.get('args', [])
        kwargs = description.get('kwargs', {})
        url_mods = description.get('url_mods', {})
        name_pieces = str(description.get('module', '')).split('.')
        module_name = '.'.join(name_pieces[:-1])
        class_name = name_pieces[-1]
        return Plugin.safely_create_plugin(module_name, class_name, args, kwargs, url_mods)

    @staticmethod
    def safely_create_plugin(module_name, class_name, args, kwargs, url_mods):
        try:
            return Plugin.create_plugin(module_name, class_name, args, kwargs, url_mods)
        except RuntimeError as ex:
            plugin_info = "\n\tclass: {}\n\tin module: {}".format(class_name, module_name)
            raise RuntimeError(str(ex)+plugin_info)

    @staticmethod
    def create_plugin(module_name, class_name, args, kwargs, url_mods):
        return Plugin.modded_config_from(
            Plugin.config_from(
                Plugin.obj_from(
                    Plugin.class_from(
                        Plugin.module_from(
                            module_name
                        ), class_name
                    ), args, kwargs
                )
            ), url_mods
        )

    @staticmethod
    def module_from(module_name):
        if module_name not in modules:
            Plugin.load_module(module_name)
        return modules[module_name]

    @staticmethod
    def load_module(module_name):
        try:
            importlib.import_module(module_name)
        except ValueError as ex:
            raise RuntimeError("Error importing module: {}".format(str(ex)))

    @staticmethod
    def class_from(module, class_name):
        try:
            return getattr(module, class_name)
        except AttributeError as ex:
            raise RuntimeError("Error loading class: {}".format(str(ex)))

    @staticmethod
    def obj_from(plugin_class, args, kwargs):
        try:
            return plugin_class(*args, **kwargs)
        except TypeError as ex:
            template = "Error creating instance: {}\n\targs: {}\n\tkwargs: {}"
            message = template.format(str(ex), str(args), str(kwargs))
            raise RuntimeError(message)

    @staticmethod
    def config_from(obj):
        if not hasattr(obj, 'config') or not isinstance(obj.config, dict):
            raise RuntimeError("Error in plugin: no config dict")
        return obj.config

    @staticmethod
    def modded_config_from(config, url_mods):
        result = config.copy()
        for source_glob, dest_path in url_mods.items():
            path = source_glob.lstrip('/').split('/')
            matches = Plugin.search_resources(config, path)
            for source_path in matches:
                Plugin.path_transform(result, source_path, dest_path)
        return result

    @staticmethod
    def search_resources(obj, search_path, resolved_path=''):
        if not search_path:
            return [resolved_path]
        if not isinstance(obj, dict):
            return []
        matches_dict = Plugin.filtered_dict(search_path[0], obj)
        result = []
        for matching_key in matches_dict:
            result += Plugin.search_resources(matches_dict[matching_key], search_path[1:], resolved_path+'/'+matching_key)
        return result

    @staticmethod
    def filtered_dict(glob, dictionary):
        return {key: dictionary[key] for key in dictionary if GlobTools.match(key, glob) and not key.startswith('#')}

    @staticmethod
    def path_transform(obj, source_path, dest_path):
        Plugin.set_recursive(obj, dest_path.strip('/').split('/'),
                             Plugin.__pop_recursive(obj, source_path.strip('/').split('/')))

    @staticmethod
    def get_recursive(dictionary, keys):
        if not keys:
            return dictionary
        if not isinstance(dictionary, dict) or keys[0] not in dictionary:
            raise KeyError(keys)
        return Plugin.get_recursive(dictionary[keys[0]], keys[1:])

    @staticmethod
    def set_recursive(dictionary, keys, value):
        if not keys:
            dictionary = value
        if len(keys) == 1:
            if not isinstance(dictionary.get(keys[0], None), dict):
                dictionary[keys[0]] = {}
                #todo warn overwrite
            if isinstance(value, dict):
                dictionary[keys[0]].update(value)
            else:
                dictionary[keys[0]] = value
            return
        if keys[0] not in dictionary:
            dictionary[keys[0]] = {}
        Plugin.set_recursive(dictionary[keys[0]], keys[1:], value)

    @staticmethod
    def __pop_recursive(dictionary, path):
        if not path:
            result = dictionary.copy()
            del dictionary
            return result
        key_piece = path[0]
        if key_piece not in dictionary:
            raise KeyError(key_piece)
        value = dictionary.pop(key_piece)
        if len(path) == 1:
            return value
        if not isinstance(value, dict):
            raise KeyError()
        return Plugin.__pop_recursive(value, path[1:])
