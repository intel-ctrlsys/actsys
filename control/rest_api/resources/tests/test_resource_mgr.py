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
from ..resource_mgr import ResourceManager, ResourceManagerException
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

class TestResourceManager(TestCase):
    """ Class for testing ResourceManager class """
    def setUp(self):
        self.cmd_invoker = MagicMock(spec=CommandInvoker)
        self.node_regex = dict(single='node01',
                               multiple='node01,node02',
                               invalid='foo',
                              )
        self.rmgr = ResourceManager()
        self.result = dict(default=CommandResult(),
                           device=CommandResult(8, device_name=self.node_regex['single']),
                           success=CommandResult(0, "Success"),
                           plugin_not_installed=CommandResult(-2, "Rmgr not installed."),
                           bad_param=CommandResult(5, 'Invalid node')
                          )

    def test__debug_msg__no_debug(self):
        """ Test debug_msg function when debug is disabled """
        mock_print_and_test(self.rmgr, self.node_regex['single'], False)

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


    def __test_mock_functions__(self, rmgr, debug_ip, port, status='drain'):
        self.assertIsNotNone(rmgr)
        self.assertTrue(rmgr.dfx)
        ret_dict = rmgr.__mock_remove_nodes__(self.node_regex['multiple'])
        expected = dict(ip=debug_ip, port=port, status=status)
        self.assertEqual(expected, ret_dict)

    def __check_remove_nodes_error__(self, cmd_invoker, node, return_code, message):
        rmgr = ResourceManager(cmd_invoker=cmd_invoker)
        ret = rmgr.__remove_nodes__(node)
        self.assertEqual(return_code, ret.return_code)
        self.assertEqual(message, ret.message)

    def test__remove_nodes__no_command_invoker(self):
        self.__check_remove_nodes_error__(None, self.node_regex['single'],
                                          409, 'No CommandInvoker available.')

    def test__remove_nodes__(self):
        self.cmd_invoker.resource_remove.return_value = self.result['success']
        self.__check_remove_nodes_error__(self.cmd_invoker, self.result['success'].device_name,
                                          self.result['success'].return_code, self.result['success'].message)

    def test__create_put_remove_response__None_dictionaries(self):
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
        success = create_dict_from_result(self.result['success'])
        ret = self.rmgr.__create_put_remove_response__(success, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.assertEqual(expected, ret)

    def test__create_put_remove_response__multiple_success(self):
        dict_successes = {self.result['success'].device_name:[self.result['success'],
                                                              self.result['success']]}
        ret = self.rmgr.__create_put_remove_response__(dict_successes, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.assertEqual(expected, ret)

    def __check_exception__(self, exception, exp_error_code, exp_message, exp_response):
        self.assertEqual(exp_error_code, exception.error_code)
        self.assertEqual(exp_message, exception.message)
        self.assertEqual(exp_response, exception.response)

    def test__create_put_remove_response__failure_bad_param_01(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, create_dict_from_result(self.result['default']))
        expected = {self.result['default'].device_name:dict(return_code=400, status='invalid')}
        self.__check_exception__(cmgr.exception, 400, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__failure_bad_param_02(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, create_dict_from_result(self.result['bad_param']))
        expected = {self.result['bad_param'].device_name:dict(return_code=400, status='invalid')}
        self.__check_exception__(cmgr.exception, 400, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__failure(self):
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='not_drain')}
        self.__check_exception__(cmgr.exception, 404, 'Could not remove node(s).', expected)

    def test__create_put_remove_response__multiple_failures(self):
        dict_failures = deepcopy(create_dict_from_result(self.result['device']))
        dict_failures.update(create_dict_from_result(self.result['bad_param']))
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, dict_failures)
        expected = {self.result['device'].device_name:dict(return_code=404, status='not_drain'),
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
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__(create_dict_from_result(self.result['success']),
                                                     create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='not_drain'),
                    self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.__check_exception__(cmgr.exception, 207, 'Could not remove some nodes.', expected)

    def test_create_put_resource_mgr_not_installed(self):
        """ Test put function with dfx disabled """
        with self.assertRaises(ResourceManagerException) as cmgr:
            self.rmgr.__create_put_remove_response__({}, \
                create_dict_from_result(self.result['plugin_not_installed']))
        self.assertEqual(424, cmgr.exception.error_code)
        self.assertIn('Resource Manager plugin is not installed.', cmgr.exception.message)

def create_test_app(dfx, debug):
    """ Creates the test client app """
    flask = Flask(__name__)
    api = Api(flask)
    api.add_resource(ResourceManager, '/resource', \
        '/resource/<string:subcommand>', \
        endpoint='resource', \
        resource_class_kwargs={'dfx':dfx, 'debug':debug})
    flask.config['TESTING'] = True
    return flask.test_client()

class TestResourceManagerFlask(TestCase):
    """ Class for testing ResourceManager class using Flask """
    def setUp(self):
        self.test_app = create_test_app(False, True)
        self.test_app_dfx = create_test_app(True, True)
        self.base_url = '/resource'
        self.url = dict(remove=self.base_url+'/remove',
                        invalid=self.base_url+'/subcommand'
                       )
        self.rmgr = ResourceManager(dfx=True)
        self.node_regex = dict(single='node01', multiple='node01,node02',
                               invalid='foo')

    def __check_response__(self, response, status_code, message):
        self.assertEqual(status_code, response.status_code)
        self.assertIn(message, response.get_data())

    def test_get(self):
        """ Test get function """
        ret = self.test_app.get(self.base_url)
        self.__check_response__(ret, 405, 'method is not allowed')

    def test_put_no_subcommand_None_node_regex(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.base_url, data=dict(node_regex=None))
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_no_subcommand_no_data(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.base_url)
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_no_subcommand_None_data(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.base_url, data=None)
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_no_subcommand_empty_data(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.base_url, data=dict())
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_no_subcommand_with_data(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.base_url,
                                data=dict(node_regex=self.node_regex['invalid']))
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_invalid_subcommand_with_data(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.url['invalid'],
                                data=dict(node_regex=self.node_regex['invalid']))
        self.__check_response__(ret, 400, 'Invalid subcommand')

    def test_put_dfx_remove_with_data(self):
        """ Test put function with dfx enabled """
        ret = self.test_app_dfx.put(self.url['remove'],
                                    data=dict(node_regex=self.node_regex['single']))
        self.assertEqual(200, ret.status_code)
        self.assertEqual(self.rmgr.__mock_remove_nodes__(self.node_regex['single']),
                         json.loads(ret.get_data()))

    def test_put_remove_invalid_node_regex(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.url['remove'],
                                data=dict(node_regex=self.node_regex['invalid']))
        self.__check_response__(ret, 404, 'Could not remove node(s).')
        print (ret.get_data())
