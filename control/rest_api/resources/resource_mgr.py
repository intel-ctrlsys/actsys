# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module to handle Resource Manager related requests """
from flask_restful import Resource
from flask import jsonify, make_response, request
from mock import create_autospec

from ...cli.command_invoker import CommandInvoker
from ..utils.utils import split_command_results, print_msg, Usage
from ...commands.command import CommandResult
from ...plugin.manager import PluginManagerException

RETURN_ERRORS = {'bad_param':[-1, 1, 5],
                 'plugin_not_installed':[-2],
                }

class ResourceManager(Resource):
    """ Resource Manager Resource Class """

    def __init__(self, cmd_invoker=None, debug=False, dfx=False,
                 dfx_data=None):
        super(ResourceManager, self).__init__()
        self.cmd_invoker = cmd_invoker if isinstance(cmd_invoker, CommandInvoker) else None
        self.debug = debug
        self.dfx = dfx
        if self.dfx:
            self._setup_mocks(dfx_data)
        self.usage = ResourceManagerUsage()

    def _setup_mocks(self, dfx_data):
        if not dfx_data:
            self.mock_debug_ip = "192.168.1.100"
            self.mock_port = 0
        else:
            self.mock_debug_ip = dfx_data.get('debug_ip', '192.168.1.100')
            self.mock_port = dfx_data.get('port', 0)
        self._mock_remove_nodes = _create_mock_fn(self._remove_nodes, \
            self.mock_debug_ip, self.mock_port, 'drain')
        self._mock_check_status = _create_mock_fn_check_status(self._check_status)
        self._mock_add_nodes = _create_mock_fn(self._add_nodes, \
            self.mock_debug_ip, self.mock_port, 'idle')

    def _debug_msg(self, message):
        if self.debug:
            print_msg(ResourceManager.__name__, message)


    def get(self, subcommand=None):
        """ Method to handle HTTP GET Requests """

        node_regex = request.args.get('node_regex', '')
        self._debug_msg('subcommand: {} node_regex: {}'.format(subcommand, node_regex))

        if subcommand in ['add', 'remove']:
            return self._invalid_method_response('GET', subcommand)

        get_function = getattr(self, '_get_{}_subcommand'.format(subcommand), None)

        if get_function:
            return get_function(subcommand, node_regex)

        return _create_response(400, 'Invalid subcommand: {0}'.format(subcommand),
                                dict(usage=self.usage.get_resource_usage_msg()))


    def _get_check_subcommand(self, subcommand, node_regex):
        if self.dfx:
            return jsonify(self._mock_check_status(node_regex))
        return self._handle_subcommand(subcommand, node_regex, self._check_status,
                                       _create_http_check_response)


    def put(self, subcommand=None):
        """ Method to handle HTTP PUT Requests """

        node_regex = request.args.get('node_regex', '')
        self._debug_msg('subcommand: {} node_regex: {}'.format(subcommand, node_regex))

        if subcommand in ['check']:
            return self._invalid_method_response('PUT', subcommand)

        put_function = getattr(self, '_put_{}_subcommand'.format(subcommand), None)

        if put_function:
            return put_function(subcommand, node_regex)

        return _create_response(400, 'Invalid subcommand: {0}'.format(subcommand),
                                dict(usage=self.usage.get_resource_usage_msg()))

    def _put_remove_subcommand(self, subcommand, node_regex):
        if self.dfx:
            return jsonify(self._mock_remove_nodes(node_regex))
        return self._handle_subcommand(subcommand, node_regex, self._remove_nodes,
                                       self._create_http_remove_response)


    def _put_add_subcommand(self, subcommand, node_regex):
        if self.dfx:
            return jsonify(self._mock_add_nodes(node_regex))
        return self._handle_subcommand(subcommand, node_regex, self._add_nodes,
                                       self._create_http_add_response)


    def _invalid_method_response(self, method, subcommand):
        return _create_response(405, method + ' method not allowed for ' + subcommand + ' option.',
                                dict(usage=self.usage.get_subcommand_usage_msg(subcommand)))

    def _check_status(self, node_regex):
        _raise_if_is_empty(node_regex, "Invalid node_regex.", 400)
        self._raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_check(node_regex)

    def _remove_nodes(self, node_regex):
        self._raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_remove(node_regex)

    def _add_nodes(self, node_regex):
        _raise_if_is_empty(node_regex, "Invalid node_regex.", 400)
        self._raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_add(node_regex)

    def _create_http_remove_response(self, successes, failures):
        return self._create_http_response_('remove', successes, failures)

    def _create_http_add_response(self, successes, failures):
        return self._create_http_response_('add', successes, failures)

    def _create_http_response_(self, subcommand, successes, failures):
        _raise_if_is_none(successes, 'Could not parse command results.')
        _raise_if_is_none(failures, 'Could not parse command results.')
        response = dict()
        self._fill_response_from_successes(response, successes)
        self._fill_response_from_failures(response, failures)
        _raise_if_is_empty(response, 'Could not parse command results.')
        if successes and not failures:
            return response
        if failures and not successes:
            _raise_if_is_single_failure(response, 'Could not ' + subcommand + ' node(s).')
            _raise_all_failed(response, 'Could not ' + subcommand + ' node(s).')
        raise ResourceManagerException(207, 'Could not ' + subcommand + ' some nodes.', response)

    def _add_failure(self, response, node, fail):
        _raise_if_plugin_not_installed(fail)
        if fail.return_code in RETURN_ERRORS['bad_param']:
            response[node] = dict(return_code=400, status='invalid', error="Invalid node_regex.")
        else:
            node_status = get_nodes_status(self._check_status(node))
            response[node] = dict(return_code=404, status=node_status.get(node, 'invalid'),
                                  error=fail.message)

    def _fill_response_from_successes(self, response, successes):
        for node in successes:
            node_status = get_nodes_status(self._check_status(node))
            response[node] = dict(return_code=200, status=node_status.get(node, 'invalid'))

    def _fill_response_from_failures(self, response, failures):
        for node in failures:
            if not isinstance(failures[node], list):
                self._add_failure(response, node, failures[node])
            else:
                for fail in failures[node]:
                    self._add_failure(response, node, fail)

    def _raise_if_no_cmd_invoker(self):
        """ Raise ResourceManagerException if there's no command invoker available"""
        if not self.cmd_invoker:
            raise ResourceManagerException(409, 'No CommandInvoker available.')

    def _handle_subcommand(self, subcommand, node_regex, subcommand_fn, response_fn):
        try:
            if subcommand == 'check':
                return jsonify(response_fn(subcommand_fn(node_regex)))
            success, fail = split_command_results(subcommand_fn(node_regex))
            return jsonify(response_fn(success, fail))
        except ResourceManagerException as rme:
            self._add_usage_message(subcommand, rme)
            return _create_response_from_exception(rme)
        except PluginManagerException as pme:
            rme = ResourceManagerException(424, 'Resource Manager plugin is not installed. \n' + pme.message)
            return _create_response_from_exception(rme)
        except Exception as unhandled_ex:
            return _create_response_from_exception(unhandled_ex)

    def _add_usage_message(self, subcommand, exception):
        if exception.error_code == 400:
            if exception.response is None:
                exception.response = dict(usage=self.usage.get_subcommand_usage_msg(subcommand))
            if isinstance(exception.response, dict):
                exception.response['usage'] = self.usage.get_subcommand_usage_msg(subcommand)


def _raise_if_plugin_not_installed(results):
    """ Raise ResourceManagerException if the resource manager plugin nis not installed """
    if not isinstance(results, list):
        results = [results]
    for result in results:
        if result.return_code in RETURN_ERRORS['plugin_not_installed']:
            raise ResourceManagerException(424, 'Resource Manager plugin is not installed.')

def _raise_if_is_single_failure(response, message=""):
    """ Raise ResourceManagerException if there's only one failure. """
    if len(response.keys()) == 1:
        item = response.itervalues().next()
        raise ResourceManagerException(item['return_code'], message, response)

def _raise_all_failed(response, message="", error_code=404):
    """ Raise ResourceManagerException, as all the commands failed. """
    raise ResourceManagerException(error_code, message, response)

def _raise_if_is_none(value, message="", error_code=409):
    """ Raise ResourceManagerException if the parameter is None. """
    if value is None:
        raise ResourceManagerException(error_code, message)

def _raise_if_is_empty(param, message="", error_code=409):
    """ Raise ResourceManagerException if the parameter is None or empty. """
    if not param:
        raise ResourceManagerException(error_code, message)

def _raise_if_all_are_invalid(node_status_dict):
    """ Raise ResourceManagerException if all the nodes in node_status_dict
        have 'invalid' as their status"""
    if node_status_dict.values().count('invalid') == len(node_status_dict):
        raise ResourceManagerException(404, 'Could not get node(s) status.', node_status_dict)

def _raise_if_invalid(node_status_dict):
    """ Raise ResourceManagerException if at least one of the nodes in node_status_dict
        has 'invalid' as its status """
    if node_status_dict.values().count('invalid') != 0:
        raise ResourceManagerException(207, 'Could not get some node(s) status.', node_status_dict)

def _create_http_check_response(results):
    _raise_if_is_none(results, 'Could not parse command results.')
    _raise_if_plugin_not_installed(results)
    node_status_dict = get_nodes_status(results)
    _raise_if_all_are_invalid(node_status_dict)
    _raise_if_invalid(node_status_dict)
    return node_status_dict

def _create_response_from_exception(exception):
    """ Creates Flask response from a ResourceManagerException """
    return _create_response(getattr(exception, 'error_code', 404),
                            getattr(exception, 'message', ""),
                            getattr(exception, 'response', None))

def _create_response(error_code, message="", data=None):
    if not data:
        return make_response(message + '\n', error_code)
    data['message'] = message
    return make_response(jsonify(data), error_code)

def _parse_node_status(result):
    """ Parses the node status from a CommandResult """
    return result.message if result.return_code == 0 else 'invalid'

def get_nodes_status(results):
    """ Gets the nodes status from a CommandResult or a list of CommandResults """
    if not isinstance(results, list):
        results = [results]
    return _get_nodes_status_from_list(results)

def _get_nodes_status_from_list(result_list):
    """ Gets the nodes status from a list of CommandResults
        and creates a dictionary with them """
    ret_dict = {}
    for result in result_list:
        if isinstance(result, CommandResult):
            ret_dict[result.device_name] = _parse_node_status(result)
    return ret_dict

def _create_mock_fn_check_status(base_fn):
    """ Creates mock function for check_status function """
    ret_dict = dict(node1='idle', node2='drain', node3='alloc', node4='invalid')
    return create_autospec(base_fn, return_value=ret_dict)

def _create_mock_fn(base_fn, debug_ip, port, status=''):
    """ Creates mock function for the base_fn function """
    ret_dict = dict(ip=debug_ip, port=port, status=status)
    return create_autospec(base_fn, return_value=ret_dict)

class ResourceManagerException(Exception):
    """ Class to raise ResourceManager Errors """
    def __init__(self, error_code=404, message="", response=None):
        super(ResourceManagerException, self).__init__(super)
        self.error_code = error_code
        self.message = message
        self.response = response


class ResourceManagerUsage(Usage):
    """ Class to manage usage messages for the ResourceManager """

    def __init__(self):
        super(ResourceManagerUsage, self).__init__()
        self._add = '/add'
        self._check = '/check'
        self._remove = '/remove'
        self._put = 'PUT'
        self._get = 'GET'
        self._subcommand = self._literals['subcommand']
        self._subcommand_desc = "\t<subcommand> could be 'add' (PUT), 'remove' (PUT) or 'check' (GET) options.\n"
        self._set_default_values()

    def _set_default_values(self):
        self._literals['command'] = '/resource'
        self._literals['command_desc'] = ''
        self._literals['args'] = self._literals['node_regex']
        self._literals['args_desc'] = self._literals['node_regex_desc']

    def _create_subcommand_usage_msg(self, subcommand, http_method, subcommand_desc=''):
        self._literals['subcommand'] = subcommand
        self._literals['http_method'] = http_method+'\n\t'
        self._literals['subcommand_desc'] = subcommand_desc
        return self.get_usage_msg()

    def _get_add_usage_msg(self):
        """ Return usage message for 'add' subcommand"""
        self._literals['description'] = "\n Add nodes to the resource manager.\n"
        return self._create_subcommand_usage_msg(self._add, self._put)

    def _get_remove_usage_msg(self):
        """ Return usage message for 'remove' subcommand"""
        self._literals['description'] = "\n Remove nodes from the resource manager.\n"
        return self._create_subcommand_usage_msg(self._remove, self._put)

    def _get_check_usage_msg(self):
        """ Return usage message for 'check' subcommand"""
        self._literals['description'] = "\n Check resource manager nodes's status.\n"
        return self._create_subcommand_usage_msg(self._check, self._get)

    def get_resource_usage_msg(self):
        """ Return usage message for resource command. """
        self._literals['description'] = "\n Resource Manager commands.\n"
        return self._create_subcommand_usage_msg(self._subcommand, self._get+'|'+self._put, self._subcommand_desc)

    def get_subcommand_usage_msg(self, subcommand=None):
        """ Return usage message for the given subcommand """
        if subcommand == 'remove':
            return self._get_remove_usage_msg()
        if subcommand == 'add':
            return self._get_add_usage_msg()
        if subcommand == 'check':
            return self._get_check_usage_msg()
        return self.get_resource_usage_msg()
