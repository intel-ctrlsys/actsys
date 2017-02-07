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
    def __init__(self, flags=None, dfx_data=None, host=None, port=None):
        if flags and isinstance(flags, dict):
            self.__set_flags_from_dict__(flags)
        else:
            self.__set_flags_to__(False)
        self.__set_dfx_vars_from_dict__(dfx_data)
        self.host = host
        self.port = port
        self.cmd_invoker = None if self.dfx else CommandInvoker()
        self.flask_app = Flask(__name__)
        self.rest_api = Api(self.flask_app)
        self.__load_config__()
        self.__add_resources__()

    def __set_flags_to__(self, value):
        self.dfx = value
        self.debug = value

    def __set_flags_from_dict__(self, flags):
        self.dfx = flags.get('dfx', False)
        self.debug = flags.get('debug', False)

    def __set_dfx_vars_from_dict__(self, dfx_data):
        if not dfx_data or not isinstance(dfx_data, dict) or \
            dfx_data.get("resource_mgr") is None:
            self.dfx_resource_mgr = self.dfx
        else:
            self.dfx_resource_mgr = dfx_data.get("resource_mgr")

    def __load_config__(self):
        self.flask_app.config.from_object(__name__)

    def __add_resources__(self):
        self.rest_api.add_resource(ResourceManager, \
            '/resource', '/resource/<string:subcommand>', \
            resource_class_kwargs={'cmd_invoker':self.cmd_invoker, \
            'dfx':self.dfx_resource_mgr, 'debug': self.debug})

    def run(self):
        """ Runs the rest api application """
        self.flask_app.run(host=self.host, port=self.port, debug=self.debug)
