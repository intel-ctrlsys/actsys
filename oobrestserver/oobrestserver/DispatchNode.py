# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Defines the DispatchNode class.

DispatchNode provides a tree model of values in the system.

DispatchNode objects load from a config dict and recursively instantiate more
nodes to build out the tree. If the #obj directive occurs in the config, the
node loads a plugin and grafts the plugin-provided paths onto the tree "here"
"""

from oobrestserver import GlobTools
from oobrestserver import Plugin


class DispatchNode(object):
    """Dispatch node for finding providers at URL routes."""

    def __init__(self, logger, config=None, base_route='', saved_plugins=None):
        self.logger = logger
        self.config = config or {}
        self.route = base_route
        self.saved_plugins = saved_plugins or {}
        self.children = {}
        self.define_plugins()
        self.load_plugins()
        self.add_children()
        self.add_getter()

    def define_plugins(self):
        plugin_descriptions = self.config.get('_define_plugins', [])
        for plugin_name in plugin_descriptions:
            plugin_description = plugin_descriptions[plugin_name]
            try:
                plugin_object = Plugin.plugin(plugin_description)
            except RuntimeError as ex:
                exception_string = "\n\t".join(str(ex).splitlines())
                self.logger.warn("Could not instantiate plugin from: "+str(plugin_description)+exception_string)
                continue
            self.saved_plugins[plugin_name] = plugin_object

    def load_plugins(self):
        for plugin_description in self.config.get('_attach_plugins', []):
            if isinstance(plugin_description, dict):
                try:
                    plugin_object = Plugin.plugin(plugin_description)
                except RuntimeError as ex:
                    exception_string = "\n\t".join(str(ex).splitlines())
                    self.logger.warn("Could not instantiate plugin from: "+str(plugin_description)+exception_string)
                    continue
            else:
                if plugin_description not in self.saved_plugins:
                    self.logger.warn("Plugin name not previously defined: "+str(plugin_description))
                    continue
                self.logger.info("loading a previously-defined plugin")
                plugin_object = self.saved_plugins[plugin_description]
            self.config.update(plugin_object)

    def add_children(self):
        for child in [x for x in self.config if not x.startswith('_') and not x.startswith('#')]:
            child_route = '/'.join([self.route, child])
            if self.route == '':
                child_route = child
            self.children[child] = DispatchNode(self.logger, self.config[child], base_route=child_route,
                                                saved_plugins=self.saved_plugins)

    def add_getter(self):
        if '#getter' not in self.config:
            self.config['#getter'] = self.subtrees
            self.config['#units'] = 'PathNode'

    def subtrees(self):
        return list(self.children.keys())

    def dispatch(self, vpath):
        try:
            if not vpath:
                return [self]
            if '**' in vpath[0]:
                return self.descendants_matching('/'.join(vpath))
            return sum([child.dispatch(vpath[1:]) for child in self.children_matching(vpath[0])], [])
        except ValueError:
            return []

    def get_method(self, label):
        func = self.config.get(label, None)
        if func is None:
            raise RuntimeError('Method not supported')
        return func

    def cleanup(self):
        self.config.get('#cleanup', lambda: None)()
        for child in self.children:
            self.children[child].cleanup()

    def children_matching(self, glob):
        return [self.children[route] for route in GlobTools.glob_filter(self.children, glob)]

    def descendants_matching(self, glob):
        return [node for node in self.descendants() if GlobTools.glob_match(node.route, glob)]

    def descendants(self):
        descendant_lists = [self.children[x].descendants() for x in self.children]
        return sum(descendant_lists, [self])
