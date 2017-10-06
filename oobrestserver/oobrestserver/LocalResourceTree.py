# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Defines the ResourceTree class.

ResourceTree provides a tree model of values in the system.

ResourceTree objects load from a config dict and recursively instantiate more
nodes to build out the tree.
"""

from oobrestserver.BaseResourceTree import BaseResourceTree
from oobrestserver.RemoteResourceTree import RemoteResourceTree
from oobrestserver import GlobTools
from oobrestserver import Plugin


class LocalResourceTree(BaseResourceTree):
    """Tree model of resources provided by plugins."""

    def __init__(self, logger, config=None, base_route='', saved_plugins=None):
        self.logger = logger
        self.config = config or {}
        self.route = base_route
        self.saved_plugins = saved_plugins or {}
        self.children = {}
        self.__define_plugins()
        self.__load_plugins()
        self.__add_children()
        self.__add_getter()

    def list_children(self, recursive=False):
        if recursive:
            descendant_lists = [child.list_children(True) for child in self.children.values()]
            return sum(descendant_lists, [self])
        return list(self.children.values())

    def get_method(self, label):
        func = self.config.get(label, None)
        if func is None:
            raise RuntimeError('Method not supported')
        return func

    def add_resources(self, config):
        raise NotImplementedError()

    def remove_resources(self, path):
        raise NotImplementedError()

    def cleanup(self):
        self.config.get('#cleanup', lambda: None)()
        for child in self.children.values():
            child.cleanup()

    def dispatch(self, vpath):
        if not vpath:
            return [self]
        if '**' in vpath[0]:
            return self._globstar_dispatch(vpath)
        results = [self.children[route].dispatch(vpath[1:]) for route in GlobTools.glob_filter(self.children, vpath[0])]
        return sum(results, [])

    def __define_plugins(self):
        plugin_descriptions = self.config.get('_define_plugins', {})
        for plugin_name, plugin_description in plugin_descriptions.items():
            plugin_object = self.__get_plugin_from_description(plugin_description)
            if plugin_object is not None:
                self.saved_plugins[plugin_name] = plugin_object

    def __load_plugins(self):
        for plugin_description in self.config.get('_attach_plugins', []):
            if isinstance(plugin_description, dict):
                plugin_object = self.__get_plugin_from_description(plugin_description)
                if plugin_object is not None:
                    self.config.update(plugin_object)
            else:
                if plugin_description not in self.saved_plugins:
                    self.logger.warn("Plugin name not previously defined: "+str(plugin_description))
                    continue
                self.logger.info("loading a previously-defined plugin")
                plugin_object = self.saved_plugins[plugin_description]
                self.config.update(plugin_object)

    def __attach_remotes(self):
        for remote_label, remote_host in self.config.get('_remote_hosts').items():
            self.children[remote_label] = RemoteResourceTree(remote_host)

    def __get_plugin_from_description(self, plugin_description):
        try:
            return Plugin.plugin(plugin_description)
        except RuntimeError as ex:
            exception_string = "\n\t".join(str(ex).splitlines())
            self.logger.warn("Could not instantiate plugin from: "+str(plugin_description)+exception_string)
            return None

    def __add_children(self):
        for child in [x for x in self.config if not x.startswith('_') and not x.startswith('#')]:
            child_route = '/'.join([self.route, child])
            if self.route == '':
                child_route = child
            self.children[child] = LocalResourceTree(self.logger, self.config[child], base_route=child_route,
                                                     saved_plugins=self.saved_plugins)

    def __add_getter(self):
        if '#getter' not in self.config:
            self.config['#getter'] = self.__get
            self.config['#units'] = 'PathNode'

    def __get(self, recursive=False):
        return [x.route for x in self.list_children(recursive)]
