# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Contains the Application class, which represents the running server."""

import cherrypy

from oobrestserver.DispatchNode import DispatchNode
from oobrestserver.GuiDispatcher import GuiDispatcher
from oobrestserver.Authenticator import Authenticator


class Application(object):
    """Main class defining the server object to be mounted to cherrypy"""

    def __init__(self, config):
        """Start the server with default settings and the specified config."""
        self.json_app = DispatchNode(config)
        self.gui_app = GuiDispatcher(self.json_app)
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
        """
        Create an Authenticator and hook up its authenticate method to
        cherrypy.
        """
        auth = Authenticator()
        try:
            auth.load(auth_file)
        except IOError:
            auth.create_empty_auth_file(auth_file)
            auth.load(auth_file)
        sec_settings = {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': lambda realm, user, password: auth.authenticate(user, password)
        }
        self.json_conf['/'].update(sec_settings)
        self.gui_conf['/'].update(sec_settings)

    def mount(self):
        cherrypy.tree.mount(self.json_app, '/api', self.json_conf)
        cherrypy.tree.mount(self.gui_app, '/gui', self.gui_conf)

    def cleanup(self):
        self.json_app.cleanup()
