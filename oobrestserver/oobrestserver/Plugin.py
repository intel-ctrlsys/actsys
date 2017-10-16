# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Provides the plugin function, which returns a fully-constructed plugin dictionary
whose terminal symbols are functions within loaded, initialized plugins.
"""

import importlib
from sys import modules

from oobrestserver import GlobTools


def plugin(description):
    args = description.get('args', [])
    kwargs = description.get('kwargs', {})
    url_mods = description.get('url_mods', {})
    name_pieces = str(description.get('module', '')).split('.')
    module_name = '.'.join(name_pieces[:-1])
    class_name = name_pieces[-1]
    return safely_create_plugin(module_name, class_name, args, kwargs, url_mods)

def safely_create_plugin(module_name, class_name, args, kwargs, url_mods):
    try:
        return create_plugin(module_name, class_name, args, kwargs, url_mods)
    except RuntimeError as ex:
        plugin_info = "\n\tclass: {}\n\tin module: {}".format(class_name, module_name)
        raise RuntimeError(str(ex)+plugin_info)

def create_plugin(module_name, class_name, args, kwargs, url_mods):
    return modded_config_from(
        config_from(
            obj_from(
                class_from(
                    module_from(
                        module_name
                    ), class_name
                ), args, kwargs
            )
        ), url_mods
    )

def load_module(module_name):
    try:
        importlib.import_module(module_name)
    except ValueError as ex:
        raise RuntimeError("Error importing module: {}".format(str(ex)))

def module_from(module_name):
    if module_name not in modules:
        load_module(module_name)
    return modules[module_name]

def class_from(module, class_name):
    try:
        return getattr(module, class_name)
    except AttributeError as ex:
        raise RuntimeError("Error loading class: {}".format(str(ex)))

def obj_from(plugin_class, args, kwargs):
    try:
        return plugin_class(*args, **kwargs)
    except TypeError as ex:
        template = "Error creating instance: {}\n\targs: {}\n\tkwargs: {}"
        message = template.format(str(ex), str(args), str(kwargs))
        raise RuntimeError(message)

def config_from(obj):
    if not hasattr(obj, 'config') or not isinstance(obj.config, dict):
        raise RuntimeError("Error in plugin: no config dict")
    return obj.config

def modded_config_from(config, url_mods):
    result = config.copy()
    for source_glob, dest_glob in url_mods.items():
        source_path = keys(source_glob)
        dest_path = keys(dest_glob)
        matches = search_resources(result, source_path)
        for resolved_source_glob in matches:
            resolved_source_path = keys(resolved_source_glob)
            path_transform(result, resolved_source_path, dest_path)
    return result

def search_resources(obj, search_path, resolved_path=''):
    if not search_path:
        return [resolved_path]
    if not isinstance(obj, dict):
        return []
    matches_dict = filtered_dict(search_path[0], obj)
    result = []
    for matching_key in matches_dict:
        result += search_resources(matches_dict[matching_key], search_path[1:], resolved_path+'/'+matching_key)
    return result

def filtered_dict(glob, dictionary):
    return {key: dictionary[key] for key in dictionary if GlobTools.glob_match(key, glob) and not key.startswith('#')}

def keys(string_path):
    return [key for key in string_path.lstrip('/').split('/') if key != '']

def path_transform(obj, source_path, dest_path):
    popped_resource_tree = __pop_recursive(obj, source_path)
    set_recursive(obj, dest_path, popped_resource_tree)

def get_recursive(dictionary, keys):
    if not keys:
        return dictionary
    if not isinstance(dictionary, dict) or keys[0] not in dictionary:
        raise KeyError(keys)
    return get_recursive(dictionary[keys[0]], keys[1:])

def set_recursive(dictionary, keys, value):
    if not keys:
        dictionary.update(value)
        return
    if keys[0] not in dictionary or not isinstance(dictionary.get(keys[0], None), dict):
        dictionary[keys[0]] = {}
    if len(keys) == 1:
        dictionary[keys[0]].update(value)
    else:
        set_recursive(dictionary[keys[0]], keys[1:], value)

def __pop_recursive(dictionary, path):
    if not path:
        result = dictionary.copy()
        del dictionary
        return result
    key_piece = path[0]
    if key_piece not in dictionary:
        raise KeyError(key_piece)
    if len(path) == 1:
        return {key_piece: dictionary.pop(key_piece)}
    value = dictionary[key_piece]
    if not isinstance(value, dict):
        raise KeyError()
    return __pop_recursive(value, path[1:])
