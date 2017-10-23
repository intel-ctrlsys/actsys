# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Contains the Application class, which represents the running server."""

import logging

import cherrypy

from oobrestserver.ResourceTree import ResourceTree
from oobrestserver.GuiWrapper import GuiWrapper
from oobrestserver.Authenticator import Authenticator
from oobrestserver import ResponseBuilder


class Application(object):
    """Main class defining the server object to be mounted to cherrypy"""

    exposed = True

    def __init__(self, config, logger=None):
        """Start the server with default settings and the specified config."""
        self.__logger = logger or logging.getLogger()
        self.tree = ResourceTree(self.__logger, config)
        self.nodes = [self.tree]
        cherrypy.engine.subscribe('stop', self.tree.cleanup)
        self.json_conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json;charset=utf-8')]
            }
        }

    def enable_auth(self, auth_file):
        """Turn on HTTP Basic Auth capabilities, with the identities found in the auth_file"""
        auth = Authenticator()
        auth.load_or_create(auth_file)
        sec_settings = {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': lambda realm, user, password: auth.authenticate(user, password)
        }
        self.json_conf['/'].update(sec_settings)

    def mount(self):
        cherrypy.tree.mount(self, '/api', self.json_conf)
        cherrypy.tree.mount(GuiWrapper(), '/gui', {'/':cherrypy.config.defaults})

    def _cp_dispatch(self, vpath):
        self.nodes = self.tree.dispatch(vpath)
        del vpath[:]
        return self

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, **url_params):
        """Invoke the #getter method for some plugin-provided resources"""
        method_kwargs = self.method_kwargs_from(url_params)
        request_kwargs = self.request_kwargs_from(url_params)
        self.__logger.info('Incoming GET request\n\tNodes: {}\n\tRequest params: {}\n\tGetter method kwargs: {}'.format(
            [node.route for node in self.nodes], request_kwargs, method_kwargs
        ))
        result = ResponseBuilder.generate_document(self.nodes, '#getter', [], method_kwargs, request_kwargs)
        self.nodes = [self.tree]
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, **url_params):
        """Invoke the #setter method for some plugin-provided resources"""
        method_kwargs = self.method_kwargs_from(url_params)
        request_kwargs = self.request_kwargs_from(url_params)
        method_args = [cherrypy.request.json]
        self.__logger.info('Incoming POST request\n\tNodes: {}\n\tRequest params: {}\n\tSetter method kwargs: {}\n\tPOSTed value: {}'.format(
            [node.route for node in self.nodes], request_kwargs, method_kwargs, cherrypy.request.json
        ))
        result = ResponseBuilder.generate_document(self.nodes, '#setter', method_args, method_kwargs, request_kwargs)
        self.nodes = [self.tree]
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        """Extend the resource tree with new configuration"""
        config = cherrypy.request.json
        for node in self.nodes:
            node.add_resources(config)
        self.nodes = [self.tree]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def DELETE(self):
        """Remove a portion of the resource tree"""
        deleted_nodes = []
        for node in self.nodes:
            parent_route = node.route.split('/')[:-1]
            parents = self.tree.dispatch(parent_route)
            leaf_obj_name = node.route.split('/')[-1]
            assert len(parents) == 1
            deleted_nodes.append(node.route)
            parent = parents[0]
            parent.remove_resources(leaf_obj_name)
        result = {'deleted': deleted_nodes}
        self.nodes = [self.tree]
        return result

    @staticmethod
    def request_kwargs_from(url_params):
        """Find the URL parameters that affect the server's treatment of the request"""
        result = {}
        if 'sample_rate' in url_params:
            result['sample_rate'] = min(float(url_params['sample_rate']), 1000)
        if 'duration' in url_params:
            result['duration'] = float(url_params['duration'])
        if 'leaves_only' in url_params:
            result['leaves_only'] = bool(url_params['leaves_only'])
        return result

    @staticmethod
    def method_kwargs_from(url_params):
        """Find the URL parameters that propagate to the kwargs of the plugin method"""
        result = url_params.copy()
        for key in ['sample_rate', 'duration', 'leaves_only', 'timeout']:
            result.pop(key, None)
        return result
