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

from oobrestserver.RDict import RDict


def plugin(description):
    args = description.get('args', [])
    kwargs = description.get('kwargs', {})
    url_mods = description.get('url_mods', {})
    name_pieces = str(description.get('module', '')).split('.')
    module_name = '.'.join(name_pieces[:-1])
    class_name = name_pieces[-1]
    return create_plugin(module_name, class_name, args, kwargs, url_mods)


def create_plugin(module_name, class_name, args, kwargs, url_mods):
    try:
        return transform(get_config(instantiate(get_class(get_module(
            module_name), class_name), args, kwargs)), url_mods)
    except RuntimeError as ex:
        raise RuntimeError(str(ex)+"\n\tclass: {}\n\tin module: {}".format(class_name, module_name))


def get_module(module_name):
    try:
        if module_name not in modules:
            importlib.import_module(module_name)
        return modules[module_name]
    except ValueError as ex:
        raise RuntimeError("Error importing module: {}".format(str(ex)))


def get_class(module, class_name):
    try:
        return getattr(module, class_name)
    except AttributeError as ex:
        raise RuntimeError("Error loading class: {}".format(str(ex)))


def instantiate(plugin_class, args, kwargs):
    try:
        return plugin_class(*args, **kwargs)
    except TypeError as ex:
        template = "Error creating instance: {}\n\targs: {}\n\tkwargs: {}"
        raise RuntimeError(template.format(str(ex), str(args), str(kwargs)))


def get_config(obj):
    if not hasattr(obj, 'config') or not isinstance(obj.config, dict):
        raise RuntimeError("Error in plugin: no config dict")
    return obj.config


def transform(config, url_mods):
    recursive_dict = RDict(config.copy())
    for source_glob, dest_glob in url_mods.items():
        source_path = keys(source_glob)
        dest_path = keys(dest_glob)
        matches = recursive_dict.search(source_path)
        for resolved_source_path in matches:
            recursive_dict.move(resolved_source_path, dest_path)
    return recursive_dict.raw()


def keys(string_path):
    return [key for key in string_path.lstrip('/').split('/') if key != '']
