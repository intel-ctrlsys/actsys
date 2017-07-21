# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing Bios """
from __future__ import print_function
from flask_restful import Api
from unittest import TestCase
from mock import MagicMock, patch, call
from flask import Flask
from ..bios import Bios, BiosUsage
from ..resource_common import ResourceCommonException
from ....cli import CommandInvoker
from ....commands import CommandResult
from ....plugin.manager import PluginManagerException


class TestBiosUsage(TestCase):
    """ Class to test BiosUsage """

    def setUp(self):
        self.usage = BiosUsage()

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

    def test_get_default_usage_msg(self):
        self._check_usage_msg(self.usage.get_default_usage_msg())
        self._check_usage_msg(self.usage.get_subcommand_usage_msg())

    def test_get_update_usage_msg(self):
        self._check_usage_msg(self.usage._get_update_usage_msg())
        self._check_usage_msg(self.usage.get_subcommand_usage_msg('update'))



class TestBiosBase(TestCase):
    """ Base Class for Bios Testing """
    def setUp(self):
        self.cmd_invoker = MagicMock(spec=CommandInvoker)
        self.node_regex = dict(single='node01',
                               other='node02',
                               invalid='foo',
                               prefix='?node_regex='
                              )
        self.image = dict(valid='file.bin',
                          prefix='&image='
                         )
        self.bios_defaults = Bios()
        self.bios = Bios(cmd_invoker=self.cmd_invoker)
        self.result = dict(
                           device=CommandResult(255, device_name=self.node_regex['single']),
                           success=CommandResult(0, "Success", device_name=self.node_regex['single']),
                           success_other=CommandResult(0, "Success", device_name=self.node_regex['other']),
                           bad_param=CommandResult(1, 'Invalid node', device_name=self.node_regex['invalid']),
                          )
        self.http_dict = dict(
                              device=dict(return_code=404, error=self.result['device'].message),
                              success=dict(return_code=200, message=self.result['success'].message),
                              success_other=dict(return_code=200, message=self.result['success_other'].message),
                              bad_param=dict(return_code=404, error=self.result['bad_param'].message)
                             )

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


class TestBios(TestBiosBase):
    """ Class to test Bios general functions """

    def test_debug_msg_no_debug(self):
        """ Test debug_msg function when debug is disabled """
        _mock_print_and_test(self.bios_defaults, self.node_regex['single'], False)

    def test_debug_msg(self):
        """ Test debug_msg function when debug is enabled """
        bios = Bios(debug=True)
        _mock_print_and_test(bios, self.node_regex['single'], True)

    def test__init__no_params(self):
        """ Tests init function without parameters """
        bios = Bios()
        self.assertIsNotNone(bios)
        self.assertIsNone(bios.cmd_invoker)
        self.assertFalse(bios.debug)

    def test__init__cmd_invoker(self):
        """ Tests init function with  cmd invoker """
        bios = Bios(cmd_invoker=self.cmd_invoker)
        self.assertIsNotNone(bios)
        self.assertEqual(self.cmd_invoker, bios.cmd_invoker)

    def test__init__debug(self):
        """ Tests init function with debug enabled """
        bios = Bios(debug=True)
        self.assertIsNotNone(bios)
        self.assertTrue(bios.debug)

    def test_add_usage_message_response_none(self):
        exception = ResourceCommonException(400)
        self.bios._add_usage_message('update', exception)
        self.assertIsNotNone(exception.response)
        self.assertIn('usage', exception.response)

    def test_add_usage_message_response_no_dict(self):
        exception = ResourceCommonException(400, "bar", "foo")
        self.bios._add_usage_message('update', exception)
        self.assertEqual('foo', exception.response)



class TestBiosFlask(TestBiosBase):
    """ Class for testing Bios class using Flask """
    def setUp(self):
        super(TestBiosFlask, self).setUp()
        self.test_app = _create_test_app(True, self.cmd_invoker)
        self.base_url = '/bios'
        self.url = dict(update=self.base_url+'/update',
                        invalid=self.base_url+'/subcommand'
                       )

    def test_get_no_subcommand_no_args(self):
        """ Test get function """
        ret = self.test_app.get(self.base_url)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_no_subcommand_no_args(self):
        ret = self.test_app.put(self.base_url)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_get_no_subcommand_none_node_regex(self):
        args = self.node_regex['prefix']
        ret = self.test_app.get(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_no_subcommand_none_node_regex(self):
        args = self.node_regex['prefix']
        ret = self.test_app.put(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_get_no_subcommand_empty_node_regex(self):
        args = self.node_regex['prefix'] + '""'
        ret = self.test_app.get(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_no_subcommand_empty_node_regex(self):
        args = self.node_regex['prefix'] + '""'
        ret = self.test_app.put(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_get_no_subcommand_with_args(self):
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.get(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_no_subcommand_with_args(self):
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.base_url + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_get_invalid_subcommand_with_args(self):
        args = self.node_regex['prefix'] + self.node_regex['invalid'] \
               + self.image['prefix'] + self.image['valid']
        ret = self.test_app.get(self.url['invalid'] + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_put_invalid_subcommand_with_args(self):
        args = self.node_regex['prefix'] + self.node_regex['invalid']
        ret = self.test_app.put(self.url['invalid'] + args)
        self._check_response(ret, 400, 'Invalid subcommand')
        self._check_response(ret, 400, 'Usage')

    def test_plugin_not_installed_exception(self):
        args = self.node_regex['prefix'] + self.node_regex['single'] \
               + self.image['prefix'] + self.image['valid']
        self.cmd_invoker.bios_update.side_effect = PluginManagerException("plugin not installed")
        ret = self.test_app.put(self.url['update'] + args)
        self._check_response(ret, 424, 'Bios plugin is not installed')

    def test_put_update_invalid_node_regex(self):
        self.cmd_invoker.bios_update.return_value = self.result['bad_param']
        args = self.node_regex['prefix'] + self.node_regex['invalid'] \
               + self.image['prefix'] + self.image['valid']
        ret = self.test_app.put(self.url['update'] + args)
        self._check_response(ret, 404, 'Could not update node(s)')

    def test_put_update_empty_image(self):
        args = self.node_regex['prefix'] + self.node_regex['single'] + self.image['prefix']
        ret = self.test_app.put(self.url['update'] + args)
        self._check_response(ret, 400, 'image parameter was not provided.')


    def test_get_update_invalid_method(self):
        args = self.node_regex['prefix'] + self.node_regex['single']
        ret = self.test_app.get(self.url['update'] + args)
        self._check_response(ret, 405, 'GET method not allowed for update option.')
        self._check_response(ret, 405, 'Usage')

def _mock_print_and_test(bios, msg, should_print):
    """ Mocks the builtin print function and checks for a given message """
    with patch('__builtin__.print') as mock_print:
        bios._debug_msg(msg)
        if should_print:
            mock_print.assert_has_calls(
                [
                    call(' * {0} - {1}'.format(bios.__class__.__name__, msg))
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



def _create_test_app(debug, cmd_invoker=None):
    """ Creates the test client app """
    flask = Flask(__name__)
    api = Api(flask)
    api.add_resource(Bios, '/bios', '/bios/', \
        '/bios/<string:subcommand>', \
        endpoint='resource', \
        resource_class_kwargs={'debug':debug, 'cmd_invoker':cmd_invoker})
    flask.config['TESTING'] = True
    return flask.test_client()


def create_dict_from_result(result):
    """ Creates a dictionary based on a CommandResult object. """
    ret = {}
    if result and isinstance(result, CommandResult):
        ret[result.device_name] = result
    return ret
