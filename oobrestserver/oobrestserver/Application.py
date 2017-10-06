# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Contains the Application class, which represents the running server."""

import logging

import cherrypy

from oobrestserver.LocalResourceTree import LocalResourceTree
from oobrestserver.GuiWrapper import GuiWrapper
from oobrestserver.Authenticator import Authenticator
from oobrestserver import ResponseBuilder


class Application(object):
    """Main class defining the server object to be mounted to cherrypy"""

    exposed = True

    def __init__(self, config, logger=None):
        """Start the server with default settings and the specified config."""
        self.logger = logger or logging.getLogger()
        self.tree = LocalResourceTree(self.logger, config)
        self.nodes = []
        self.gui_app = GuiWrapper(self)
        cherrypy.engine.subscribe('stop', self.cleanup)
        self.json_conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json;charset=utf-8')]
            }
        }
        self.gui_conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/html;charset=utf-8')]
            }
        }

    def enable_auth(self, auth_file):
        auth = Authenticator()
        auth.load_or_create(auth_file)
        sec_settings = {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': lambda realm, user, password: auth.authenticate(user, password)
        }
        self.json_conf['/'].update(sec_settings)
        self.gui_conf['/'].update(sec_settings)

    def mount(self):
        cherrypy.tree.mount(self, '/api', self.json_conf)
        cherrypy.tree.mount(self.gui_app, '/gui', self.gui_conf)

    def cleanup(self):
        self.tree.cleanup()

    def _cp_dispatch(self, vpath):
        self.nodes = self.tree.dispatch(vpath)
        del vpath[:]
        return self

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, **url_params):
        method_kwargs = self.method_kwargs_from(url_params)
        request_kwargs = self.request_kwargs_from(url_params)
        return ResponseBuilder.generate_document(self.nodes, '#getter', [], method_kwargs, request_kwargs)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, **url_params):
        method_kwargs = self.method_kwargs_from(url_params)
        request_kwargs = self.request_kwargs_from(url_params)
        method_args = [cherrypy.request.json]
        return ResponseBuilder.generate_document(self.nodes, '#setter', method_args, method_kwargs, request_kwargs)

    @staticmethod
    def request_kwargs_from(url_params):
        result = {}
        if 'sample_rate' in url_params:
            result['sample_rate'] = min(float(url_params['sample_rate']), 1000)
        if 'duration' in url_params:
            result['duration'] = float(url_params['duration'])
        if 'leaves_only' in url_params:
            result['leaves_only'] = bool(url_params['leaves_only'])
        if 'timeout' in url_params:
            result['timeout'] = float(url_params['timeout'])
        return result

    @staticmethod
    def method_kwargs_from(url_params):
        result = url_params.copy()
        for key in ['sample_rate', 'duration', 'leaves_only', 'timeout']:
            result.pop(key, None)
        return result
