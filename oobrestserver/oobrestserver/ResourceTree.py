# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Defines the ResourceTree class.
ResourceTree provides a tree model of values in the system.
ResourceTree objects load from a config dict and recursively instantiate more
nodes to build out the tree.
"""
from collections import Hashable
from oobrestserver import GlobTools
from oobrestserver import Plugin


class ResourceTree(object):
    """Tree model of resources provided by plugins."""

    def __init__(self, logger, config=None, base_route='', saved_plugins=None):
        self.logger = logger
        self.route = base_route
        self.saved_plugins = saved_plugins or {}
        self.children = {}
        self.properties = {}
        self.add_resources(config)

    def list_children(self, recursive=False):
        if recursive:
            descendant_lists = [child.list_children(True) for child in self.children.values()]
            return sum(descendant_lists, [self])
        return list(self.children.values())

    def get_property(self, label):
        return self.properties.get(label, None)

    def add_resources(self, config):
        self.__define_plugins(config)
        self.__attach_plugins(config)
        self.__attach_children(config)
        self.__set_own_properties(config)

    def __define_plugins(self, config):
        for plugin_name, plugin_description in config.get('_define_plugins', {}).items():
            plugin_object = self.__get_plugin(plugin_description)
            if plugin_object is not None:
                self.saved_plugins[plugin_name] = plugin_object

    def __attach_plugins(self, config):
        for plugin_description in config.get('_attach_plugins', []):
            plugin_object = self.__get_plugin(plugin_description)
            config.update(plugin_object or {})

    def __attach_children(self, config):
        for child in [x for x in config if not x.startswith('_') and not x.startswith('#')]:
            child_route = '/'.join([self.route, child])
            if self.route == '':
                child_route = child
            self.children[child] = ResourceTree(self.logger, config[child], base_route=child_route,
                                                saved_plugins=self.saved_plugins)

    def __set_own_properties(self, config):
        for node_property in [key for key in config if key.startswith('#')]:
            self.properties[node_property] = config[node_property]
        if '#getter' not in config:
            self.properties['#getter'] = self.__get
            self.properties['#units'] = 'PathNode'

    def __get_plugin(self, plugin_description):
        try:
            if isinstance(plugin_description, Hashable) and plugin_description is not None:
                if plugin_description in self.saved_plugins:
                    return self.saved_plugins[plugin_description]
                raise RuntimeError("Plugin not previously defined")
            elif isinstance(plugin_description, dict):
                return Plugin.plugin(plugin_description)
            raise RuntimeError("Plugin description not dict or Hashable")
        except RuntimeError as ex:
            exception_string = "\n\t".join(str(ex).splitlines())
            self.logger.warn("Could not instantiate plugin from: "+str(plugin_description)+exception_string)

    def remove_resources(self, child):
        if child in self.children:
            del self.children[child]

    def cleanup(self):
        self.properties.get('#cleanup', lambda: None)()
        for child in self.children.values():
            child.cleanup()

    def dispatch(self, vpath):
        """Return list of all nodes matching the vpath according to glob semantics."""
        if not vpath:
            return [self]
        if '**' in vpath[0]:
            return self._globstar_dispatch(vpath)
        results = [self.children[route].dispatch(vpath[1:]) for route in GlobTools.glob_filter(self.children, vpath[0])]
        return sum(results, [])

    def __get(self, recursive=False):
        return [x.route for x in self.list_children(recursive)]

    def _globstar_dispatch(self, vpath):
        children = self.list_children(True)
        return [node for node in children if GlobTools.glob_match(node.route, '/'.join(vpath))]
