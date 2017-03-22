# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
This module creates a rest application to execute user commands.
"""
from flask_restful import Api
from flask import Flask
from .resources.resource_mgr import ResourceManager
from ..cli.command_invoker import CommandInvoker

class ControlRestApi(object):
    """ Class that creates a rest application to execute user commands. """
    def __init__(self, **kwargs):
        self._set_flags_from_kwargs(kwargs)
        self.cmd_invoker = None if self.dfx else CommandInvoker()
        self.flask_app = Flask(__name__)
        self.rest_api = Api(self.flask_app)
        self._load_config()
        self._add_resources()

    def _set_flags_from_kwargs(self, kwargs):
        self.dfx = kwargs.get('dfx', False)
        self.debug = kwargs.get('debug', False)
        self.dfx_resource_mgr = kwargs.get('dfx_resource_mgr', self.dfx)
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')

    def _load_config(self):
        self.flask_app.config.from_object(__name__)

    def _add_resources(self):
        self.rest_api.add_resource(ResourceManager, \
            '/resource', '/resource/', '/resource/<string:subcommand>', \
            resource_class_kwargs={'cmd_invoker':self.cmd_invoker, \
            'dfx':self.dfx_resource_mgr, 'debug': self.debug})

    def run(self):
        """ Runs the rest api application """
        self.flask_app.run(host=self.host, port=self.port, debug=self.debug)
