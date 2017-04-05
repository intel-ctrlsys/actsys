# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module to handle Resource Manager related requests """
from flask import jsonify
from mock import create_autospec

from ..utils.utils import split_command_results, Usage
from ...commands.command import CommandResult
from ...plugin.manager import PluginManagerException

from .resource_common import ResourceCommon, ResourceCommonException
from .resource_common import HTTP

RETURN_ERRORS = {'bad_param':[-1, 1, 5],
                 'plugin_not_installed':[-2],
                }

class ResourceManager(ResourceCommon):
    """ Resource Manager Resource Class """

    def __init__(self, cmd_invoker=None, debug=False, dfx=False,
                 dfx_data=None):
        super(ResourceManager, self).__init__(cmd_invoker, debug, dfx, dfx_data)
        self.usage = ResourceManagerUsage()
        self.valid_commands = ['check', 'add', 'remove']

    def _setup_mocks(self, dfx_data):
        if not dfx_data:
            self.mock_debug_ip = "192.168.1.100"
            self.mock_port = 0
        else:
            self.mock_debug_ip = dfx_data.get('debug_ip', '192.168.1.100')
            self.mock_port = dfx_data.get('port', 0)
        self._mock_remove_nodes = self._create_mock_fn(self._remove_nodes, \
            self.mock_debug_ip, self.mock_port, 'drain')
        self._mock_check_status = self._create_mock_fn_check_status(self._check_status)
        self._mock_add_nodes = self._create_mock_fn(self._add_nodes, \
            self.mock_debug_ip, self.mock_port, 'idle')

    def _get_check_subcommand(self, subcommand, node_regex):
        if self.dfx:
            return jsonify(self._mock_check_status(node_regex))
        return self._handle_subcommand(subcommand, node_regex, self._check_status,
                                       self._create_http_check_response)

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

    def _check_status(self, node_regex):
        self._raise_if_is_empty(node_regex, "Invalid node_regex.", HTTP.BAD_REQUEST)
        self._raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_check(node_regex)

    def _remove_nodes(self, node_regex):
        self._raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_remove(node_regex)

    def _add_nodes(self, node_regex):
        self._raise_if_is_empty(node_regex, "Invalid node_regex.", HTTP.BAD_REQUEST)
        self._raise_if_no_cmd_invoker()
        return self.cmd_invoker.resource_add(node_regex)

    def _create_http_remove_response(self, successes, failures):
        return self._create_http_response_('remove', successes, failures)

    def _create_http_add_response(self, successes, failures):
        return self._create_http_response_('add', successes, failures)


    def _add_failure(self, response, node, fail):
        self._raise_if_plugin_not_installed(fail)
        if fail.return_code in RETURN_ERRORS['bad_param']:
            response[node] = dict(return_code=HTTP.BAD_REQUEST, status='invalid', error="Invalid node_regex.")
        else:
            node_status = self.get_nodes_status(self._check_status(node))
            response[node] = dict(return_code=HTTP.NOT_FOUND, status=node_status.get(node, 'invalid'),
                                  error=fail.message)

    def _fill_response_from_successes(self, response, successes):
        for node in successes:
            node_status = self.get_nodes_status(self._check_status(node))
            response[node] = dict(return_code=HTTP.STATUS_OK, status=node_status.get(node, 'invalid'))

    def _fill_response_from_failures(self, response, failures):
        for node in failures:
            if not isinstance(failures[node], list):
                self._add_failure(response, node, failures[node])
            else:
                for fail in failures[node]:
                    self._add_failure(response, node, fail)

    def _handle_subcommand(self, subcommand, node_regex, subcommand_fn, response_fn):
        try:
            if subcommand == 'check':
                return jsonify(response_fn(subcommand_fn(node_regex)))
            success, fail = split_command_results(subcommand_fn(node_regex))
            return jsonify(response_fn(success, fail))
        except ResourceCommonException as rme:
            self._add_usage_message(subcommand, rme)
            return self._create_response_from_exception(rme)
        except PluginManagerException as pme:
            rme = ResourceCommonException(HTTP.FAILED_DEPENDENCY,
                                          'Resource Manager plugin is not installed. \n'
                                          + pme.message)
            return self._create_response_from_exception(rme)
        except Exception as unhandled_ex:
            return self._create_response_from_exception(unhandled_ex)

    def _add_usage_message(self, subcommand, exception):
        if exception.error_code == HTTP.BAD_REQUEST:
            if exception.response is None:
                exception.response = dict(usage=self.usage.get_subcommand_usage_msg(subcommand))
            if isinstance(exception.response, dict):
                exception.response['usage'] = self.usage.get_subcommand_usage_msg(subcommand)

    @classmethod
    def _create_http_check_response(cls, results):
        cls._raise_if_is_none(results, 'Could not parse command results.')
        cls._raise_if_plugin_not_installed(results)
        node_status_dict = cls.get_nodes_status(results)
        cls._raise_if_all_are_invalid(node_status_dict)
        cls._raise_if_invalid(node_status_dict)
        return node_status_dict

    @classmethod
    def _raise_if_plugin_not_installed(cls, results):
        """ Raise ResourceCommonException if the resource manager plugin is not installed """
        if not isinstance(results, list):
            results = [results]
        for result in results:
            if result.return_code in RETURN_ERRORS['plugin_not_installed']:
                raise ResourceCommonException(HTTP.FAILED_DEPENDENCY,
                                              'Resource Manager plugin is not installed.')

    @classmethod
    def _raise_if_all_are_invalid(cls, node_status_dict):
        """ Raise ResourceCommonException if all the nodes in node_status_dict
            have 'invalid' as their status"""
        if node_status_dict.values().count('invalid') == len(node_status_dict):
            raise ResourceCommonException(HTTP.NOT_FOUND, 'Could not get node(s) status.', node_status_dict)

    @classmethod
    def _raise_if_invalid(cls, node_status_dict):
        """ Raise ResourceCommonException if at least one of the nodes in node_status_dict
            has 'invalid' as its status """
        if node_status_dict.values().count('invalid') != 0:
            raise ResourceCommonException(HTTP.MULTI_STATUS,
                                          'Could not get some node(s) status.',
                                          node_status_dict)

    @classmethod
    def _parse_node_status(cls, result):
        """ Parses the node status from a CommandResult """
        return result.message if result.return_code == 0 else 'invalid'

    @classmethod
    def _get_nodes_status_from_list(cls, result_list):
        """ Gets the nodes status from a list of CommandResults
            and creates a dictionary with them """
        ret_dict = {}
        for result in result_list:
            if isinstance(result, CommandResult):
                ret_dict[result.device_name] = cls._parse_node_status(result)
        return ret_dict

    @classmethod
    def get_nodes_status(cls, results):
        """ Gets the nodes status from a CommandResult or a list of CommandResults """
        if not isinstance(results, list):
            results = [results]
        return cls._get_nodes_status_from_list(results)

    @classmethod
    def _create_mock_fn_check_status(cls, base_fn):
        """ Creates mock function for check_status function """
        ret_dict = dict(node1='idle', node2='drain', node3='alloc', node4='invalid')
        return create_autospec(base_fn, return_value=ret_dict)

    @classmethod
    def _create_mock_fn(cls, base_fn, debug_ip, port, status=''):
        """ Creates mock function for the base_fn function """
        ret_dict = dict(ip=debug_ip, port=port, status=status)
        return create_autospec(base_fn, return_value=ret_dict)

    def get(self, subcommand=None):
        """ Handles HTTP GET requests"""
        return self.dispatch_requests(self.valid_commands, subcommand, 'get')

    def put(self, subcommand=None):
        """ Handles HTTP PUT requests"""
        return self.dispatch_requests(self.valid_commands, subcommand, 'put')

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
        self._subcommand_desc = "\t<subcommand> could be 'add' (PUT), " + \
                                "'remove' (PUT) or 'check' (GET) options.\n"
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

    def get_default_usage_msg(self):
        """ Return usage message for resource command. """
        self._literals['description'] = "\n Resource Manager commands.\n"
        return self._create_subcommand_usage_msg(self._subcommand,
                                                 self._get + '|' + self._put, self._subcommand_desc)
