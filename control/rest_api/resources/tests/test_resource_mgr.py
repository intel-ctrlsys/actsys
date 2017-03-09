# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing ResourceManager """
from __future__ import print_function
from flask_restful import Api
from unittest import TestCase
from copy import deepcopy
from mock import MagicMock, patch, call
from flask import Flask, json
from ..resource_mgr import ResourceManager, ResourceManagerException, get_nodes_status
from ....cli import CommandInvoker
from ....commands import CommandResult

def mock_print_and_test(rmgr, msg, should_print):
    """ Mocks the builtin print function and checks for a given message """
    with patch('__builtin__.print') as mock_print:
        rmgr.__debug_msg__(msg)
        if should_print:
            mock_print.assert_has_calls(
                [
                    call(' * {0} - {1}'.format(rmgr.__class__.__name__, msg))
                ]
            )
        else:
            mock_print.assert_not_called()

def create_dict_from_result(result):
    """ Creates a dictionary based on a CommandResult object. """
    ret = {}
    if result and isinstance(result, CommandResult):
        ret[result.device_name] = result
    return ret

class TestResourceManagerBase(TestCase):
    """ Base Class for Resource Manager Testing """
    def setUp(self):
        self.cmd_invoker = MagicMock(spec=CommandInvoker)
        self.node_regex = dict(single='node01',
                               other='node02',
                               multiple='node01,node02',
                               invalid='foo',
                               prefix='?node_regex='
                              )
        self.rmgr_defaults = ResourceManager()
        self.rmgr = ResourceManager(cmd_invoker=self.cmd_invoker)
        self.rmgr_dfx = ResourceManager(dfx=True)
        self.result = dict(default=CommandResult(),
                           device=CommandResult(8, device_name=self.node_regex['single']),
                           success=CommandResult(0, "Success", device_name=self.node_regex['other']),
                           plugin_not_installed=CommandResult(-2, "Rmgr not installed."),
                           bad_param=CommandResult(1, 'Invalid node'),
                           idle=CommandResult(0, 'idle', self.node_regex['single']),
                           drain=CommandResult(0, 'drain', self.node_regex['other']),
                           alloc=CommandResult(0, 'alloc')
                          )

    def __test_mock_functions__(self, rmgr, debug_ip, port, status='drain'):
        self.assertIsNotNone(rmgr)
        self.assertTrue(rmgr.dfx)
        ret_dict = rmgr.__mock_remove_nodes__(self.node_regex['multiple'])
        expected = dict(ip=debug_ip, port=port, status=status)
        self.assertEqual(expected, ret_dict)
        ret_dict = rmgr.__mock_check_status__(self.node_regex['multiple'])
        expected = dict(node1='idle', node2='drain', node3='alloc', node4='invalid')
        self.assertEqual(expected, ret_dict)

    def __check_result__(self, result, return_code, message):
        self.assertEqual(return_code, result.return_code)
        self.assertEqual(message, result.message)

    def __check_exception__(self, exception, exp_error_code, exp_message, exp_response=None, nested=True):
        self.assertEqual(exp_error_code, exception.error_code)
        self.assertEqual(exp_message, exception.message)
        if nested:
            self.assertTrue(check_exception_response(exp_response if exp_response else {}, exception.response))
        else:
            self.assertEqual(exception.response, exp_response)

    def __check_response__(self, response, status_code, message):
        self.assertEqual(status_code, response.status_code)
        self.assertIn(message, response.get_data())


class TestResourceManager(TestResourceManagerBase):
    """ Class to test ResourceManager general functions """

    def test__debug_msg__no_debug(self):
        """ Test debug_msg function when debug is disabled """
        mock_print_and_test(self.rmgr_defaults, self.node_regex['single'], False)

    def test__debug_msg__(self):
        """ Test debug_msg function when debug is enabled """
        rmgr = ResourceManager(debug=True)
        mock_print_and_test(rmgr, self.node_regex['single'], True)

    def test__init__no_params(self):
        """ Tests init function without parameters """
        rmgr = ResourceManager()
        self.assertIsNotNone(rmgr)
        self.assertIsNone(rmgr.cmd_invoker)
        self.assertFalse(rmgr.dfx)
        self.assertFalse(rmgr.debug)

    def test__init__cmd_invoker(self):
        """ Tests init function with  cmd invoker """
        rmgr = ResourceManager(cmd_invoker=self.cmd_invoker)
        self.assertIsNotNone(rmgr)
        self.assertEqual(self.cmd_invoker, rmgr.cmd_invoker)

    def test__init__debug(self):
        """ Tests init function with debug enabled """
        rmgr = ResourceManager(debug=True)
        self.assertIsNotNone(rmgr)
        self.assertTrue(rmgr.debug)

    def test__init__no_mock_fns(self):
        """ Tests no mock functions are created when dfx is disabled """
        rmgr = ResourceManager(dfx=False)
        self.assertIsNotNone(rmgr)
        self.assertFalse(rmgr.dfx)
        with self.assertRaises(AttributeError):
            rmgr.__mock_remove_nodes__(self.node_regex['multiple'])

    def test__init__no_mock_variables(self):
        """ Tests no mock functions are created when dfx is disabled """
        rmgr = ResourceManager(dfx=False, dfx_data=dict(debug_ip=self.node_regex['single'],
                                                        port=5))
        self.assertIsNotNone(rmgr)
        self.assertFalse(rmgr.dfx)
        with self.assertRaises(AttributeError):
            self.assertIsNone(rmgr.mock_debug_ip)
        with self.assertRaises(AttributeError):
            self.assertIsNone(rmgr.mock_port)

    def test__init__dfx_defaults(self):
        """ Tests init function with dfx enabled, default values"""
        rmgr = ResourceManager(dfx=True)
        self.__test_mock_functions__(rmgr, rmgr.mock_debug_ip, rmgr.mock_port)


    def test__init__dfx_data_provided(self):
        """ Tests init function with dfx enabled, debug_ip and port provided"""
        rmgr = ResourceManager(dfx=True, dfx_data=dict(debug_ip=self.node_regex['single'],
                                                       port=5))
        self.__test_mock_functions__(rmgr, self.node_regex['single'], 5)


class TestResourceManagerRemove(TestResourceManagerBase):
    """ Class to test remove related functions """

    def test__remove_nodes__no_command_invoker(self):
        with self.assertRaises(ResourceManagerException)as cmgr:
            self.rmgr_defaults.__remove_nodes__(self.node_regex['single'])
        self.__check_exception__(cmgr.exception, 409, 'No CommandInvoker available.')

    def test__remove_nodes__(self):
        self.cmd_invoker.resource_remove.return_value = self.result['success']
        ret = self.rmgr.__remove_nodes__(self.result['success'].device_name)
        self.__check_result__(ret, self.result['success'].return_code,
                              self.result['success'].message)

    def test__create_put_remove_response__none_dictionaries(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__(None, None)
        self.assertEqual(409, cmgr.exception.error_code)
        self.assertEqual('Could not parse command results.', cmgr.exception.message)
        self.assertIsNone(cmgr.exception.response)

    def test__create_put_remove_response__empty_dictionaries(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, {})
        self.assertEqual(409, cmgr.exception.error_code)
        self.assertEqual('Could not parse command results.', cmgr.exception.message)
        self.assertIsNone(cmgr.exception.response)

    def test__create_put_remove_response__single_success(self):
        self.cmd_invoker.resource_check.return_value = self.result['drain']
        success = create_dict_from_result(self.result['success'])
        ret = self.rmgr.__create_put_remove_response__(success, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.assertEqual(expected, ret)

    def test__create_put_remove_response__multiple_success(self):
        self.cmd_invoker.resource_check.return_value = [self.result['drain'], self.result['drain']]
        dict_successes = {self.result['success'].device_name:[self.result['success'],
                                                              self.result['success']]}
        ret = self.rmgr.__create_put_remove_response__(dict_successes, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.assertEqual(expected, ret)

    def test__create_put_remove_response__failure_bad_param_01(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, create_dict_from_result(self.result['default']))
        expected = {self.result['default'].device_name:dict(return_code=400, status='invalid')}
        self.__check_exception__(cmgr.exception, 400, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__failure_bad_param_02(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, create_dict_from_result(self.result['bad_param']))
        expected = {self.result['bad_param'].device_name:dict(return_code=400,
                                                              status='invalid',
                                                              error='Invalid node_regex.')}
        self.__check_exception__(cmgr.exception, 400, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__failure(self):
        self.cmd_invoker.resource_check.return_value = self.result['alloc']
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc')}
        self.__check_exception__(cmgr.exception, 404, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__multiple_failures(self):
        dict_failures = deepcopy(create_dict_from_result(self.result['device']))
        dict_failures.update(create_dict_from_result(self.result['bad_param']))
        self.cmd_invoker.resource_check.return_value = [self.result['alloc'], self.result['default']]
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, dict_failures)
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc'),
                    self.result['bad_param'].device_name:dict(return_code=400, status='invalid')}
        self.__check_exception__(cmgr.exception, 404, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__multiple_failures_same_node(self):
        dict_failures = {self.result['device'].device_name:[self.result['device'],
                                                            self.result['device']]}
        dict_failures[self.result['device'].device_name][1].return_code = -1
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, dict_failures)
        expected = {self.result['device'].device_name:dict(return_code=400, status='invalid')}
        self.__check_exception__(cmgr.exception, 400, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__mixed(self):
        self.cmd_invoker.resource_check.return_value = [self.result['alloc'], self.result['drain']]
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__(create_dict_from_result(self.result['success']),
                                                     create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc'),
                    self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.__check_exception__(cmgr.exception, 207, 'Could not remove some nodes.', expected)

    def test_create_put_resource_mgr_not_installed(self):
        """ Test put function with dfx disabled """
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, \
                create_dict_from_result(self.result['plugin_not_installed']))
        self.assertEqual(424, cmgr.exception.error_code)
        self.assertIn('Resource Manager plugin is not installed', cmgr.exception.message)


class TestResourceManagerCheck(TestResourceManagerBase):
    """ Class to test check related functions """

    def test__check_status__none(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__check_status__(None)
        self.assertEqual(409, cmgr.exception.error_code)
        self.assertIn('Invalid node_regex', cmgr.exception.message)

    def test__check_status__empty(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__check_status__("")
        self.assertEqual(409, cmgr.exception.error_code)
        self.assertIn('Invalid node_regex', cmgr.exception.message)

    def test__check_status__no_cmd_invoker(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr_defaults.__check_status__(self.node_regex['invalid'])
        self.assertEqual(409, cmgr.exception.error_code)
        self.assertIn('No CommandInvoker available', cmgr.exception.message)

    def test__check_status__(self):
        self.cmd_invoker.resource_check.return_value = self.result['idle']
        ret = self.rmgr.__check_status__(self.node_regex['single'])
        self.__check_result__(ret, self.result['idle'].return_code, self.result['idle'].message)

    def test_get_nodes_status_single_result(self):
        expected = {self.result['idle'].device_name:'idle'}
        ret = get_nodes_status(self.result['idle'])
        self.assertEqual(expected, ret)

    def test_get_nodes_status_multiple_result(self):
        expected = {self.result['idle'].device_name:'idle',
                    self.result['drain'].device_name:'drain'}
        ret = get_nodes_status([self.result['idle'], self.result['drain']])
        self.assertEqual(expected, ret)

    def test_get_nodes_status_multiple_invalid(self):
        self.assertEqual({}, get_nodes_status(['foo', 'bar']))

    def test_get_nodes_status__none(self):
        self.assertEqual({}, get_nodes_status(None))

    def test_get_nodes_status_invalid_results(self):
        self.assertEqual({}, get_nodes_status('foo'))

    def test__create_put_check_response__none(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_check_response__(None)
        self.__check_exception__(cmgr.exception, 409, 'Could not parse command results.')

    def test__create_put_check_response__single(self):
        ret = self.rmgr.__create_put_check_response__(self.result['idle'])
        expected = {self.result['idle'].device_name:self.result['idle'].message}
        self.assertEqual(expected, ret)

    def test__create_put_check_response__single_failed(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_check_response__(self.result['device'])
        expected = {self.result['device'].device_name:'invalid'}
        self.__check_exception__(cmgr.exception, 404, 'Could not get node(s) status.', expected, False)

    def test__create_put_check_response__multiple(self):
        ret = self.rmgr.__create_put_check_response__([self.result['idle'], self.result['drain']])
        expected = {self.result['idle'].device_name:self.result['idle'].message,
                    self.result['drain'].device_name:self.result['drain'].message}
        self.assertEqual(expected, ret)

    def test__create_put_check_response__multiple_failed(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_check_response__([self.result['device'], self.result['default']])
        expected = {self.result['device'].device_name:'invalid',
                    self.result['default'].device_name:'invalid'}
        self.__check_exception__(cmgr.exception, 404, 'Could not get node(s) status.', expected, False)

    def test__create_put_check_response__multiple_mix(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_check_response__([self.result['drain'], self.result['device']])
        expected = {self.result['drain'].device_name:self.result['drain'].message,
                    self.result['device'].device_name:'invalid'}
        self.__check_exception__(cmgr.exception, 207, 'Could not get some node(s) status.', expected, False)


def check_exception_response(expected, response):
    """ Checks if expected is a subset of response dictionary """
    if response:
        for node in response:
            if expected[node].items() > response[node].items():
                return False
    return True

def create_test_app(dfx, debug, cmd_invoker=None):
    """ Creates the test client app """
    flask = Flask(__name__)
    api = Api(flask)
    api.add_resource(ResourceManager, '/resource', \
        '/resource/<string:subcommand>', \
        endpoint='resource', \
        resource_class_kwargs={'dfx':dfx, 'debug':debug, 'cmd_invoker':cmd_invoker})
    flask.config['TESTING'] = True
    return flask.test_client()

class TestResourceManagerFlask(TestResourceManagerBase):
    """ Class for testing ResourceManager class using Flask """
    def setUp(self):
        super(TestResourceManagerFlask, self).setUp()
        self.test_app = create_test_app(False, True, self.cmd_invoker)
        self.test_app_dfx = create_test_app(True, True)
        self.base_url = '/resource'
        self.url = dict(remove=self.base_url+'/remove',
                        invalid=self.base_url+'/subcommand'
                       )

    def test_get(self):
        """ Test get function """
        ret = self.test_app.get(self.base_url)
        self.__check_response__(ret, 405, 'method is not allowed')

    def test_put_no_subcommand_none_node_regex(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix']
        ret = self.test_app.put(self.base_url + args)
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_no_subcommand_no_args(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.base_url)
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_no_subcommand_empty_node_regex(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + '""'
        ret = self.test_app.put(self.base_url + args)
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_no_subcommand_with_args(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.base_url + args)
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_invalid_subcommand_with_args(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.url['invalid'] + args)
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_remove_plugin_not_installed(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + self.node_regex['single']
        self.cmd_invoker.resource_remove.return_value = self.result['plugin_not_installed']
        ret = self.test_app.put(self.url['remove'] + args)
        self.__check_response__(ret, 424, 'Resource Manager plugin is not installed')


    def test_put_dfx_remove_with_args(self):
        """ Test put function with dfx enabled """
        args = self.node_regex['prefix'] + self.node_regex['single']
        ret = self.test_app_dfx.put(self.url['remove'] + args)
        self.assertEqual(200, ret.status_code)
        self.assertEqual(self.rmgr_dfx.__mock_remove_nodes__(self.node_regex['single']),
                         json.loads(ret.get_data()))

    def test_put_remove_invalid_node_regex(self):
        """ Test put function with dfx disabled """
        self.cmd_invoker.resource_remove.return_value = self.result['bad_param']
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.url['remove'] + args)
        self.__check_response__(ret, 400, 'Could not remove node(s).')
