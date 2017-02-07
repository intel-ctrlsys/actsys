# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module to handle Resource Manager related requests """
from flask_restful import Resource
from mock import create_autospec
from flask import abort, make_response, jsonify, request
from ..utils.utils import print_msg, handle_command_results
from ...cli.command_invoker import CommandInvoker
from ...commands import CommandResult

class ResourceManager(Resource):
    """ Resource Manager Resource Class """
    def __init__(self, cmd_invoker=None, debug=False, dfx=False,
                 dfx_data=None):
        super(ResourceManager, self).__init__()
        self.cmd_invoker = cmd_invoker if isinstance(cmd_invoker, CommandInvoker) else None
        self.debug = debug
        self.dfx = dfx
        if self.dfx:
            self.__setup_mocks__(dfx_data)
        self.return_errors = dict(bad_param=[-1, 1, 5],
                                  plugin_not_installed=[-2],
                                 )

    def __setup_mocks__(self, dfx_data):
        if not dfx_data:
            self.mock_debug_ip = "192.168.1.100"
            self.mock_port = 0
        else:
            self.mock_debug_ip = dfx_data.get('debug_ip', '192.168.1.100')
            self.mock_port = dfx_data.get('port', 0)
        self.__mock_remove_nodes__ = create_mock_fn_remove_nodes(self.__remove_nodes__, \
            self.mock_debug_ip, self.mock_port)

    def __debug_msg__(self, message):
        if self.debug:
            print_msg(ResourceManager.__name__, message)

    def __remove_nodes__(self, node_regex):
        if not self.cmd_invoker:
            return CommandResult(409, 'No CommandInvoker available.', device_name=node_regex)
        return self.cmd_invoker.resource_remove(node_regex, None)

    def put(self, subcommand=None):
        """ Method to handle HTTP PUT Requests """
        node_regex = request.args.get('node_regex', '')
        self.__debug_msg__('subcommand: {} node_regex: {}'.format(subcommand, node_regex))
        if subcommand == 'remove':
            if self.dfx:
                return jsonify(self.__mock_remove_nodes__(node_regex))
            success, fail = handle_command_results(self.__remove_nodes__(node_regex))
            try:
                return jsonify(self.__create_put_remove_response__(success, fail))
            except ResourceManagerException as rme:
                rme.response['message'] = rme.message
                return make_response(jsonify(rme.response), rme.error_code)
        abort(400, 'Invalid subcommand: {0}'.format(subcommand))


    def __create_put_remove_response__(self, successes, failures):
        raise_if_is_none(successes)
        raise_if_is_none(failures)
        response = dict()
        self.__fill_response_from_successes_(response, successes)
        self.__fill_response_from_failures__(response, failures)
        raise_if_is_empty(response)
        if successes and not failures:
            return response
        if failures and not successes:
            raise_if_is_single_failure(response)
            raise_all_failed(response)
        raise ResourceManagerException(207, 'Could not remove some nodes.', response)

    def __add_failure__(self, response, node, fail):
        if fail.return_code in self.return_errors['bad_param']:
            response[node] = dict(return_code=400, status='invalid')
        elif fail.return_code in self.return_errors['plugin_not_installed']:
            raise ResourceManagerException(424, 'Resource Manager plugin is not installed.')
        else:
            #TODO get the current status of the nodes and append it in response.
            response[node] = dict(return_code=404, status='not_drain')

    def __fill_response_from_successes_(self, response, successes):
        for node in successes:
            #TODO get the current status of the nodes and append it in response.
            response[node] = dict(return_code=200, status='drain')

    def __fill_response_from_failures__(self, response, failures):
        for node in failures:
            if not isinstance(failures[node], list):
                self.__add_failure__(response, node, failures[node])
            else:
                for fail in failures[node]:
                    self.__add_failure__(response, node, fail)


def raise_if_is_single_failure(response):
    """ Raise ResourceManagerException if there's only one failure. """
    if len(response.keys()) == 1:
        item = response.itervalues().next()
        raise ResourceManagerException(item['return_code'], 'Could not remove node(s).', response)

def raise_all_failed(response):
    """ Raise ResourceManagerException, as all the commands failed. """
    raise ResourceManagerException(404, 'Could not remove node(s).', response)

def raise_if_is_none(param):
    """ Raise ResourceManagerException if the parameter is None. """
    if param is None:
        raise ResourceManagerException(409, 'Could not parse command results.')

def raise_if_is_empty(param):
    """ Raise ResourceManagerException if the parameter is None or empty. """
    if not param:
        raise ResourceManagerException(409, 'Could not parse command results.')


def create_mock_fn_remove_nodes(base_fn, debug_ip, port):
    """ Creates mock function for remove_nodes function """
    ret_dict = dict(ip=debug_ip, port=port, status='drain')
    return create_autospec(base_fn, return_value=ret_dict)

class ResourceManagerException(Exception):
    """ Class to raise ResourceManager Errors """
    def __init__(self, error_code=404, message="", response=None):
        super(ResourceManagerException, self).__init__(super)
        self.error_code = error_code
        self.message = message
        self.response = response
