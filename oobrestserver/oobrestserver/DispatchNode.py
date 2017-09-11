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

import cherrypy
from oobrestserver.GlobTools import GlobTools
from oobrestserver.PluginTools import PluginTools
from oobrestserver.ResponseBuilder import ResponseBuilder


class DispatchNode(object):
    """Dispatch node for finding providers at URL routes."""

    exposed = True

    def __init__(self, config=None, base_route=''):
        self.route = base_route
        self.children = {}
        self.config = config or {}
        self.add_plugin()
        self.add_children()
        self.add_getter()

    def add_plugin(self):
        inst_args = self.config.get('#obj', None)
        if inst_args:
            try:
                obj = PluginTools.instantiate(*inst_args)
                self.config = obj.config
            except Exception as ex:
                print('Warning: Exception when importing user module ' +
                      str(inst_args) + ': ' + str(ex))

    def add_children(self):
        for child in [x for x in self.config if not x.startswith('#')]:
            child_route = '/'.join([self.route, child])
            if self.route == '':
                child_route = child
            self.children[child] = DispatchNode(self.config[child],
                                                base_route=child_route)

    def add_getter(self):
        if '#getter' not in self.config:
            self.config['#getter'] = self.get
            self.config['#units'] = 'PathNode'

    def get(self):
        return [key for key in self.children]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, **kwargs):
        return self.get(**kwargs)

    def _cp_dispatch(self, vpath):
        return ResponseBuilder(self.dispatch(vpath))

    def dispatch(self, vpath):
        # Determine the list of nodes that match the request
        if not vpath:
            return [self]
        path = vpath[:]
        glob = path.pop(0)
        try:
            if '**' in glob:
                glob = '/'.join(vpath)
                del vpath[:]
                return self.descendants_matching(glob)
            result = []
            for child in self.children_matching(glob):
                result += child.dispatch(path)
            return result
        except ValueError as val_err:
            raise cherrypy.HTTPError(status=400, message=str(val_err))

    def cleanup(self):
        func = self.config.get('#cleanup', None)
        if func:
            func()
        for child in self.children:
            self.children[child].cleanup()

    def children_matching(self, glob):
        routes = GlobTools.filter(self.children, glob)
        return [self.children[route] for route in routes]

    def descendants_matching(self, glob):
        return [node for node in self.descendants() if GlobTools.match(node.route, glob)]

    def descendants(self):
        if not self.children:
            return [self]
        descendant_lists = [self.children[x].descendants() for x in self.children]
        return [self]+[node for sublist in descendant_lists for node in sublist]
