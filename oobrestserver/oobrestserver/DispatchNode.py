"""Defines the DispatchNode class.

A DispatchNode instance is, in CherryPy terminology, a 'dispatcher', in that it
has the _cp_dispatch method. This method is how CherryPy follows URL routes to
the correct HTTP method implementations.

DispatchNode builds, from a JSON description, the whole tree model of values
provided by the server, instantiates plugin instances to provide the get/set
interfaces for each value, and makes the values available on the web service
through _cp_dispatch.

"""

from sys import modules
import importlib
import re

import cherrypy

from ResponseForm import ResponseForm
from ParallelDispatcher import ParallelDispatcher


class DispatchNode(object):
    """Dispatch node for finding providers at URL routes."""

    exposed = True

    def __init__(self, config=None, base_route=''):
        self.route = base_route
        self.children = {}
        self.config = config or {}
        self.add_plugin(self.config.get('#obj', None))
        self.add_children()

    def add_plugin(self, ctor_args):
        if not ctor_args:
            return
        obj = DispatchNode.instantiate(*ctor_args)
        self.graft_plugin_config(obj)

    def graft_plugin_config(self, obj):
        if hasattr(obj, 'config') and isinstance(obj.config, dict):
            self.config = obj.config

    def add_children(self):
        for child in [x for x in self.config if not x.startswith('#')]:
            child_route = '/'.join([self.route, child])
            if self.route == '':
                child_route = child
            self.children[child] = DispatchNode(self.config[child],
                                                base_route=child_route)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, **kwargs):
        return self.get(**kwargs)

    def get(self, **kwargs):
        func = self.config.get('#getter', None)
        return {self.route: self.dict_from_provided_method(func, **kwargs)}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        return self.set(value=cherrypy.request.json)

    def set(self, value):
        func = self.config.get('#setter', None)
        if func is None:
            response = ResponseForm()
            response.data['exceptions'] = ['Method not supported']
            return {self.route: response.finished_dict()}
        return {self.route: self.dict_from_provided_method(func, value)}

    def dict_from_provided_method(self, func, *args, **kwargs):
        """Prepare a ResponseForm from a passed method with args."""
        if func is None:
            children_dict = {}
            for child in self.children:
                children_dict[child] = self.children[child].route
            return {'children': children_dict}
        DispatchNode.check_plugin_method_callable(func)
        response = ResponseForm()
        response.data['units'] = self.config.get('#units', None)
        sample_rate = kwargs.get('sample_rate')
        duration = kwargs.get('duration')
        if duration and sample_rate:
            response.add_samples_over_time(sample_rate, duration, func, *args)
        else:
            response.add_sample_from_func(func, *args)
        return response.finished_dict()

    def _cp_dispatch(self, vpath):
        return self.to_parallel(vpath) or \
               self.to_child(vpath)

    def cleanup(self):
        func = self.config.get('#cleanup', None)
        if func and callable(func):
            func()
        for child in self.children:
            self.children[child].cleanup()


    def to_parallel(self, vpath):
        if re.search(r'[\[\]\*\?\|\(\)]', '/'.join(vpath)):
            return ParallelDispatcher(self, vpath)
        return None

    def to_child(self, vpath):
        url_piece = vpath[0]
        if url_piece in self.children:
            vpath.pop(0)
            return self.children[url_piece]

    def ls_from(self, path, leaves_only=True):
        """List all nodes under this path recursively"""
        if not self.children:
            return [path]
        result = []
        if not leaves_only:
            result.append(path)
        for child in self.children:
            new_path = path + '/' + child if path else child
            result += self.children[child].ls_from(new_path, leaves_only)
        return result

    @staticmethod
    def check_plugin_method_callable(func):
        if not callable(func):
            message = 'Plugin-provided method not callable'
            raise cherrypy.HTTPError(status=500, message=message)

    @staticmethod
    def instantiate(full_name, *args):
        """Instantiate a plugin object and return it."""
        try:
            module_name, class_name = DispatchNode.parse_name(full_name)
            if module_name not in modules:
                importlib.import_module(module_name)
            module = modules[module_name]
            cls = getattr(module, class_name)
            return cls(*args)
        except Exception as ex:
            print('Warning: Exception when importing user module ' +
                  str(full_name) + ': ' + str(ex))

    @staticmethod
    def parse_name(full_name):
        name_pieces = str(full_name).split('.')
        return '.'.join(name_pieces[:-1]), name_pieces[-1]
