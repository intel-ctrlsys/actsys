# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module to handle Resource Manager related requests """
from flask_restful import Resource
from flask import abort, jsonify, make_response, request
from mock import create_autospec

from ...cli.command_invoker import CommandInvoker
from ..utils.utils import handle_command_results, print_msg
from ...commands.command import CommandResult


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
        self.__mock_check_status__ = create_mock_fn_check_status(self.__check_status__)

    def __debug_msg__(self, message):
        if self.debug:
            print_msg(ResourceManager.__name__, message)

    def put(self, subcommand=None):
        """ Method to handle HTTP PUT Requests """
        node_regex = request.args.get('node_regex', '')
        self.__debug_msg__('subcommand: {} node_regex: {}'.format(subcommand, node_regex))
        if subcommand == 'remove':
            if self.dfx:
                return jsonify(self.__mock_remove_nodes__(node_regex))
            try:
                success, fail = handle_command_results(self.__remove_nodes__(node_regex))
                return jsonify(self.__create_put_remove_response__(success, fail))
            except ResourceManagerException as rme:
                return create_response_from_exception(rme)
        abort(400, 'Invalid subcommand: {0}'.format(subcommand))

    def __check_status__(self, node_regex):
        raise_if_is_empty(node_regex, "Invalid node_regex.")
        self.raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_check(node_regex)

    def __remove_nodes__(self, node_regex):
        self.raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_remove(node_regex)

    def __create_put_check_response__(self, results):
        raise_if_is_none(results, 'Could not parse command results.')
        self.raise_if_plugin_not_installed(results)
        node_status_dict = get_nodes_status(results)
        raise_if_all_are_invalid(node_status_dict)
        raise_if_invalid(node_status_dict)
        return node_status_dict

    def __create_put_remove_response__(self, successes, failures):
        raise_if_is_none(successes, 'Could not parse command results.')
        raise_if_is_none(failures, 'Could not parse command results.')
        response = dict()
        self.__fill_response_from_successes_(response, successes)
        self.__fill_response_from_failures__(response, failures)
        raise_if_is_empty(response, 'Could not parse command results.')
        if successes and not failures:
            return response
        if failures and not successes:
            raise_if_is_single_failure(response, 'Could not remove node(s).')
            raise_all_failed(response, 'Could not remove node(s).')
        raise ResourceManagerException(207, 'Could not remove some nodes.', response)

    def __add_failure__(self, response, node, fail):
        self.raise_if_plugin_not_installed(fail)
        if fail.return_code in self.return_errors['bad_param']:
            response[node] = dict(return_code=400, status='invalid', error="Invalid node_regex.")
        else:
            node_status = get_nodes_status(self.__check_status__(node))
            response[node] = dict(return_code=404, status=node_status.get(node, 'invalid'),
                                  error=fail.message)

    def __fill_response_from_successes_(self, response, successes):
        for node in successes:
            node_status = get_nodes_status(self.__check_status__(node))
            response[node] = dict(return_code=200, status=node_status.get(node, 'invalid'))

    def __fill_response_from_failures__(self, response, failures):
        for node in failures:
            if not isinstance(failures[node], list):
                self.__add_failure__(response, node, failures[node])
            else:
                for fail in failures[node]:
                    self.__add_failure__(response, node, fail)

    def raise_if_no_cmd_invoker(self):
        """ Raise ResourceManagerException if there's no command invoker available"""
        if not self.cmd_invoker:
            raise ResourceManagerException(409, 'No CommandInvoker available.')

    def raise_if_plugin_not_installed(self, results):
        """ Raise ResourceManagerException if the resource manager plugin nis not installed """
        if not isinstance(results, list):
            results = [results]
        for result in results:
            if result.return_code in self.return_errors['plugin_not_installed']:
                raise ResourceManagerException(424, 'Resource Manager plugin is not installed.')

def raise_if_is_single_failure(response, message=""):
    """ Raise ResourceManagerException if there's only one failure. """
    if len(response.keys()) == 1:
        item = response.itervalues().next()
        raise ResourceManagerException(item['return_code'], message, response)

def raise_all_failed(response, message=""):
    """ Raise ResourceManagerException, as all the commands failed. """
    raise ResourceManagerException(404, message, response)

def raise_if_is_none(value, message=""):
    """ Raise ResourceManagerException if the parameter is None. """
    if value is None:
        raise ResourceManagerException(409, message)

def raise_if_is_empty(param, message=""):
    """ Raise ResourceManagerException if the parameter is None or empty. """
    if not param:
        raise ResourceManagerException(409, message)

def raise_if_all_are_invalid(node_status_dict):
    """ Raise ResourceManagerException if all the nodes in node_status_dict
        have 'invalid' as their status"""
    if node_status_dict.values().count('invalid') == len(node_status_dict):
        raise ResourceManagerException(404, 'Could not get node(s) status.', node_status_dict)

def raise_if_invalid(node_status_dict):
    """ Raise ResourceManagerException if at least one of the nodes in node_status_dict
        has 'invalid' as its status """
    if node_status_dict.values().count('invalid') != 0:
        raise ResourceManagerException(207, 'Could not get some node(s) status.', node_status_dict)

def create_response_from_exception(exception):
    """ Creates Flask response from a ResourceManagerException """
    if exception.response is None:
        return make_response(exception.message, exception.error_code)
    exception.response['message'] = exception.message
    return make_response(jsonify(exception.response), exception.error_code)

def parse_node_status(result):
    """ Parses the node status from a CommandResult """
    return result.message if result.return_code == 0 else 'invalid'

def get_nodes_status(results):
    """ Gets the nodes status from a CommandResult or a list of CommandResults """
    if not isinstance(results, list):
        results = [results]
    return get_nodes_status_from_list(results)

def get_nodes_status_from_list(result_list):
    """ Gets the nodes status from a list of CommandResults
        and creates a dictionary with them """
    ret_dict = {}
    for result in result_list:
        if isinstance(result, CommandResult):
            ret_dict[result.device_name] = parse_node_status(result)
    return ret_dict

def create_mock_fn_check_status(base_fn):
    """ Creates mock function for check_status function """
    ret_dict = dict(node1='idle', node2='drain', node3='alloc', node4='invalid')
    return create_autospec(base_fn, return_value=ret_dict)

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
