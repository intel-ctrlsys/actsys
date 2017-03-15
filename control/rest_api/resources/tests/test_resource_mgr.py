# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing ResourceManager """
from __future__ import print_function
from flask_restful import Api
from unittest import TestCase
from mock import MagicMock, patch, call
from flask import Flask, json
from ..resource_mgr import ResourceManager, ResourceManagerUsage, ResourceManagerException
from ....cli import CommandInvoker
from ....commands import CommandResult

class TestResourceManagerUsage(TestCase):
    """ Class to test ResourceManagerUsage """

    def setUp(self):
        self.usage = ResourceManagerUsage()

    def _create_expected_str(self):
        return (self.usage._literals['title']+
                self.usage._literals['description']+
                self.usage._literals['usage']+
                self.usage._literals['http_method_supported']+
                self.usage._literals['http_method']+
                self.usage._literals['url']+
                self.usage._literals['command']+
                self.usage._literals['subcommand']+
                self.usage._literals['args_start']+
                self.usage._literals['args']+
                self.usage._literals['where']+
                self.usage._literals['server_desc']+
                self.usage._literals['port_desc']+
                self.usage._literals['command_desc']+
                self.usage._literals['subcommand_desc']+
                self.usage._literals['args_desc']
               )

    def _check_usage_msg(self, msg):
        self.assertEqual(self._create_expected_str(), msg)
        print (msg)

    def test_get_resource_usage_msg(self):
        self._check_usage_msg(self.usage.get_resource_usage_msg())
        self._check_usage_msg(self.usage.get_subcommand_usage_msg())

    def test_get_add_usage_msg(self):
        self._check_usage_msg(self.usage._get_add_usage_msg())
        self._check_usage_msg(self.usage.get_subcommand_usage_msg('add'))

    def test_get_remove_usage_msg(self):
        self._check_usage_msg(self.usage._get_remove_usage_msg())
        self._check_usage_msg(self.usage.get_subcommand_usage_msg('remove'))

    def test_get_check_usage_msg(self):
        self._check_usage_msg(self.usage._get_check_usage_msg())
        self._check_usage_msg(self.usage.get_subcommand_usage_msg('check'))



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
                           success=CommandResult(0, "Success", device_name=self.node_regex['single']),
                           plugin_not_installed=CommandResult(-2, "Rmgr not installed."),
                           bad_param=CommandResult(1, 'Invalid node'),
                           idle=CommandResult(0, 'idle', self.node_regex['single']),
                           drain=CommandResult(0, 'drain', self.node_regex['single']),
                           alloc=CommandResult(0, 'alloc', self.node_regex['other'])
                          )

    def _test_mock_functions(self, rmgr, debug_ip, port):
        self.assertIsNotNone(rmgr)
        self.assertTrue(rmgr.dfx)
        ret_dict = rmgr._mock_remove_nodes(self.node_regex['multiple'])
        expected = dict(ip=debug_ip, port=port, status='drain')
        self.assertEqual(expected, ret_dict)
        ret_dict = rmgr._mock_check_status(self.node_regex['multiple'])
        expected = dict(node1='idle', node2='drain', node3='alloc', node4='invalid')
        self.assertEqual(expected, ret_dict)
        ret_dict = rmgr._mock_add_nodes(self.node_regex['multiple'])
        expected = dict(ip=debug_ip, port=port, status='idle')
        self.assertEqual(expected, ret_dict)

    def _check_result(self, result, return_code, message):
        self.assertEqual(return_code, result.return_code)
        self.assertEqual(message, result.message)

    def _check_exception(self, exception, exp_error_code, exp_message, exp_response=None, nested=True):
        self.assertEqual(exp_error_code, exception.error_code)
        self.assertIn(exp_message, exception.message)
        if nested:
            self.assertTrue(_check_exception_response(exp_response if exp_response else {}, exception.response))
        else:
            self.assertEqual(exception.response, exp_response)

    def _check_response(self, response, status_code, message):
        self.assertEqual(status_code, response.status_code)
        self.assertIn(message, response.get_data())


class TestResourceManager(TestResourceManagerBase):
    """ Class to test ResourceManager general functions """

    def test_debug_msg_no_debug(self):
        """ Test debug_msg function when debug is disabled """
        _mock_print_and_test(self.rmgr_defaults, self.node_regex['single'], False)

    def test_debug_msg(self):
        """ Test debug_msg function when debug is enabled """
        rmgr = ResourceManager(debug=True)
        _mock_print_and_test(rmgr, self.node_regex['single'], True)

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
            rmgr._mock_remove_nodes(self.node_regex['multiple'])

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
        self._test_mock_functions(rmgr, rmgr.mock_debug_ip, rmgr.mock_port)


    def test__init__dfx_data_provided(self):
        """ Tests init function with dfx enabled, debug_ip and port provided"""
        rmgr = ResourceManager(dfx=True, dfx_data=dict(debug_ip=self.node_regex['single'],
                                                       port=5))
        self._test_mock_functions(rmgr, self.node_regex['single'], 5)

    def test_add_usage_message_response_none(self):
        exception = ResourceManagerException(400)
        self.rmgr._add_usage_message('add', exception)
        self.assertIsNotNone(exception.response)
        self.assertIn('usage', exception.response)


    def test_add_usage_message_response_no_dict(self):
        exception = ResourceManagerException(400, "bar", "foo")
        self.rmgr._add_usage_message('add', exception)
        self.assertEqual('foo', exception.response)

class TestResourceManagerFlask(TestResourceManagerBase):
    """ Class for testing ResourceManager class using Flask """
    def setUp(self):
        super(TestResourceManagerFlask, self).setUp()
        self.test_app = _create_test_app(False, True, self.cmd_invoker)
        self.test_app_dfx = _create_test_app(True, True)
        self.base_url = '/resource'
        self.url = dict(remove=self.base_url+'/remove',
                        add=self.base_url+'/add',
                        invalid=self.base_url+'/subcommand'
                       )

    def test_get(self):
        """ Test get function """
        ret = self.test_app.get(self.base_url)
        self._check_response(ret, 405, 'method is not allowed')

    def test_put_no_subcommand_none_node_regex(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix']
        ret = self.test_app.put(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_no_subcommand_no_args(self):
        """ Test put function with dfx disabled """
        ret = self.test_app.put(self.base_url)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_no_subcommand_empty_node_regex(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + '""'
        ret = self.test_app.put(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_no_subcommand_with_args(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_invalid_subcommand_with_args(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.url['invalid'] + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_remove_plugin_not_installed(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + self.node_regex['single']
        self.cmd_invoker.resource_remove.return_value = self.result['plugin_not_installed']
        ret = self.test_app.put(self.url['remove'] + args)
        self._check_response(ret, 424, 'Resource Manager plugin is not installed')


    def test_put_dfx_remove_with_args(self):
        """ Test put function with dfx enabled """
        args = self.node_regex['prefix'] + self.node_regex['single']
        ret = self.test_app_dfx.put(self.url['remove'] + args)
        self.assertEqual(200, ret.status_code)
        self.assertEqual(self.rmgr_dfx._mock_remove_nodes(self.node_regex['single']),
                         json.loads(ret.get_data()))

    def test_put_remove_invalid_node_regex(self):
        """ Test put function with dfx disabled """
        self.cmd_invoker.resource_remove.return_value = self.result['bad_param']
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.url['remove'] + args)
        self._check_response(ret, 400, 'Could not remove node(s).')
        self._check_response(ret, 400, 'Usage')

    def test_put_add_plugin_not_installed(self):
        """ Test put function with dfx disabled """
        args = self.node_regex['prefix'] + self.node_regex['single']
        self.cmd_invoker.resource_add.return_value = self.result['plugin_not_installed']
        ret = self.test_app.put(self.url['add'] + args)
        self._check_response(ret, 424, 'Resource Manager plugin is not installed')


    def test_put_dfx_add_with_args(self):
        """ Test put function with dfx enabled """
        args = self.node_regex['prefix'] + self.node_regex['single']
        ret = self.test_app_dfx.put(self.url['add'] + args)
        self.assertEqual(200, ret.status_code)
        self.assertEqual(self.rmgr_dfx._mock_add_nodes(self.node_regex['single']),
                         json.loads(ret.get_data()))

    def test_put_add_invalid_node_regex(self):
        """ Test put function with dfx disabled """
        self.cmd_invoker.resource_add.return_value = self.result['bad_param']
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.url['add'] + args)
        self._check_response(ret, 400, 'Could not add node(s).')
        self._check_response(ret, 400, 'Usage')


def _mock_print_and_test(rmgr, msg, should_print):
    """ Mocks the builtin print function and checks for a given message """
    with patch('__builtin__.print') as mock_print:
        rmgr._debug_msg(msg)
        if should_print:
            mock_print.assert_has_calls(
                [
                    call(' * {0} - {1}'.format(rmgr.__class__.__name__, msg))
                ]
            )
        else:
            mock_print.assert_not_called()

def _check_exception_response(expected, response):
    """ Checks if expected is a subset of response dictionary """
    if response:
        for node in response:
            if expected[node].items() > response[node].items():
                return False
    return True



def _create_test_app(dfx, debug, cmd_invoker=None):
    """ Creates the test client app """
    flask = Flask(__name__)
    api = Api(flask)
    api.add_resource(ResourceManager, '/resource', \
        '/resource/<string:subcommand>', \
        endpoint='resource', \
        resource_class_kwargs={'dfx':dfx, 'debug':debug, 'cmd_invoker':cmd_invoker})
    flask.config['TESTING'] = True
    return flask.test_client()


def create_dict_from_result(result):
    """ Creates a dictionary based on a CommandResult object. """
    ret = {}
    if result and isinstance(result, CommandResult):
        ret[result.device_name] = result
    return ret
