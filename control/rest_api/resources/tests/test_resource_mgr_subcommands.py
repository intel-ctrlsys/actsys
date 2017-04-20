# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing ResourceManager """
from __future__ import print_function
from copy import deepcopy
from ..resource_common import ResourceCommonException
from .test_resource_mgr import TestResourceManagerBase, create_dict_from_result

class TestResourceManagerRemove(TestResourceManagerBase):
    """ Class to test remove related functions """

    def test_remove_nodes_no_command_invoker(self):
        with self.assertRaises(ResourceCommonException)as cmgr:
            self.rmgr_defaults._remove_nodes(self.node_regex['single'])
        self._check_exception(cmgr.exception, 409, 'No CommandInvoker available.')

    def test_remove_nodes(self):
        self.cmd_invoker.resource_remove.return_value = self.result['success']
        ret = self.rmgr._remove_nodes(self.result['success'].device_name)
        self._check_result(ret, self.result['success'].return_code,
                           self.result['success'].message)

    def test_create_http_remove_response_none_dictionaries(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response(None, None)
        self._check_exception(cmgr.exception, 409, 'Could not parse command results.', None, False)

    def test_create_http_remove_response_empty_dictionaries(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response({}, {})
        self._check_exception(cmgr.exception, 409, 'Could not parse command results.', None, False)

    def test_create_http_remove_response_single_success(self):
        self.cmd_invoker.resource_check.return_value = self.result['drain']
        success = create_dict_from_result(self.result['success'])
        ret = self.rmgr._create_http_remove_response(success, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.assertEqual(expected, ret)

    def test_create_http_remove_response_multiple_success(self):
        self.cmd_invoker.resource_check.return_value = [self.result['drain'], self.result['drain']]
        dict_successes = {self.result['success'].device_name:[self.result['success'],
                                                              self.result['success']]}
        ret = self.rmgr._create_http_remove_response(dict_successes, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='drain')}
        self.assertEqual(expected, ret)

    def test_create_http_remove_response_failure_bad_param_01(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response({}, create_dict_from_result(self.result['default']))
        expected = {self.result['default'].device_name:dict(return_code=400, status='invalid')}
        self._check_exception(cmgr.exception, 400, 'Could not remove node(s).', expected)


    def test_create_http_remove_response_failure_bad_param_02(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response({}, create_dict_from_result(self.result['bad_param']))
        expected = {self.result['bad_param'].device_name:dict(return_code=400,
                                                              status='invalid',
                                                              error='Invalid node_regex.')}
        self._check_exception(cmgr.exception, 400, 'Could not remove node(s).', expected)

    def test_create_http_remove_response_failure(self):
        self.cmd_invoker.resource_check.return_value = self.result['alloc']
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response({}, create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc')}
        self._check_exception(cmgr.exception, 404, 'Could not remove node(s).', expected)

    def test_create_http_remove_response_multiple_failures(self):
        dict_failures = deepcopy(create_dict_from_result(self.result['device']))
        dict_failures.update(create_dict_from_result(self.result['bad_param']))
        self.cmd_invoker.resource_check.return_value = [self.result['alloc'], self.result['default']]
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response({}, dict_failures)
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc'),
                    self.result['bad_param'].device_name:dict(return_code=400, status='invalid')}
        self._check_exception(cmgr.exception, 404, 'Could not remove node(s).', expected)

    def test_create_http_remove_response_multiple_failures_same_node(self):
        dict_failures = {self.result['device'].device_name:[self.result['device'],
                                                            self.result['device']]}
        dict_failures[self.result['device'].device_name][1].return_code = -1
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response({}, dict_failures)
        expected = {self.result['device'].device_name:dict(return_code=400, status='invalid')}
        self._check_exception(cmgr.exception, 400, 'Could not remove node(s).', expected)

    def test_create_http_remove_response_mixed(self):
        self.cmd_invoker.resource_check.return_value = [self.result['alloc'], self.result['drain']]
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response(create_dict_from_result(self.result['success']),
                                                   create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc'),
                    self.result['success'].device_name:dict(return_code=200, status='drain')}
        self._check_exception(cmgr.exception, 207, 'Could not remove some nodes.', expected)

    def test_create_http_resource_mgr_not_installed(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_remove_response({}, \
                create_dict_from_result(self.result['plugin_not_installed']))
        self._check_exception(cmgr.exception, 424, 'Resource Manager plugin is not installed')


class TestResourceManagerCheck(TestResourceManagerBase):
    """ Class to test check related functions """

    def test_check_status_none(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._check_status(None)
        self._check_exception(cmgr.exception, 400, 'Invalid node_regex')

    def test_check_status_empty(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._check_status("")
        self._check_exception(cmgr.exception, 400, 'Invalid node_regex')

    def test_check_status_no_cmd_invoker(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr_defaults._check_status(self.node_regex['invalid'])
        self._check_exception(cmgr.exception, 409, 'No CommandInvoker available')

    def test_check_status(self):
        self.cmd_invoker.resource_check.return_value = self.result['idle']
        ret = self.rmgr._check_status(self.node_regex['single'])
        self._check_result(ret, self.result['idle'].return_code, self.result['idle'].message)

    def test_get_nodes_status_single_result(self):
        expected = {self.result['idle'].device_name:'idle'}
        ret = self.rmgr.get_nodes_status(self.result['idle'])
        self.assertEqual(expected, ret)

    def test_get_nodes_status_multiple_result(self):
        expected = {self.result['idle'].device_name:'idle',
                    self.result['drain'].device_name:'drain'}
        ret = self.rmgr.get_nodes_status([self.result['idle'], self.result['drain']])
        self.assertEqual(expected, ret)

    def test_get_nodes_status_multiple_invalid(self):
        self.assertEqual({}, self.rmgr.get_nodes_status(['foo', 'bar']))

    def test_get_nodes_status_none(self):
        self.assertEqual({}, self.rmgr.get_nodes_status(None))

    def test_get_nodes_status_invalid_results(self):
        self.assertEqual({}, self.rmgr.get_nodes_status('foo'))

    def test_create_http_check_response_none(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_check_response(None)
        self._check_exception(cmgr.exception, 409, 'Could not parse command results.')

    def test_create_http_check_response_single(self):
        ret = self.rmgr._create_http_check_response(self.result['idle'])
        expected = {self.result['idle'].device_name:self.result['idle'].message}
        self.assertEqual(expected, ret)

    def test_create_http_check_response_single_failed(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_check_response(self.result['device'])
        expected = {self.result['device'].device_name:'invalid'}
        self._check_exception(cmgr.exception, 404, 'Could not get node(s) status.', expected, False)

    def test_create_http_check_response_multiple(self):
        ret = self.rmgr._create_http_check_response([self.result['idle'], self.result['drain']])
        expected = {self.result['idle'].device_name:self.result['idle'].message,
                    self.result['drain'].device_name:self.result['drain'].message}
        self.assertEqual(expected, ret)

    def test_create_http_check_response_multiple_failed(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_check_response([self.result['device'], self.result['default']])
        expected = {self.result['device'].device_name:'invalid',
                    self.result['default'].device_name:'invalid'}
        self._check_exception(cmgr.exception, 404, 'Could not get node(s) status.', expected, False)

    def test_create_http_check_response_multiple_mix(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_check_response([self.result['drain'], self.result['default']])
        expected = {self.result['drain'].device_name:self.result['drain'].message,
                    self.result['default'].device_name:'invalid'}
        self._check_exception(cmgr.exception, 207, 'Could not get some node(s) status.', expected, False)


class TestResourceManagerAdd(TestResourceManagerBase):
    """ Clas for testing ResourceManager add related functions """

    def test_add_nodes_single(self):
        self.cmd_invoker.resource_add.return_value = self.result['success']
        ret = self.rmgr._add_nodes(self.result['success'].device_name)
        self._check_result(ret, self.result['success'].return_code,
                           self.result['success'].message)

    def test_add_nodes_none(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._add_nodes(None)
        self._check_exception(cmgr.exception, 400, "Invalid node_regex.")

    def test_add_nodes_empty(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._add_nodes("")
        self._check_exception(cmgr.exception, 400, "Invalid node_regex.")

    def test_add_nodes_no_cmd_invoker(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr_defaults._add_nodes(self.node_regex['single'])
        self._check_exception(cmgr.exception, 409, "No CommandInvoker available.")

    def test_create_http_add_response_none_successes(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response(None, {})
        self._check_exception(cmgr.exception, 409, 'Could not parse command results.')

    def test_create_http_add_response_none_failures(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response({}, None)
        self._check_exception(cmgr.exception, 409, 'Could not parse command results.')

    def test_create_http_add_response_single_success(self):
        self.cmd_invoker.resource_check.return_value = self.result['idle']
        success = create_dict_from_result(self.result['success'])
        ret = self.rmgr._create_http_add_response(success, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='idle')}
        self.assertEqual(expected, ret)

    def test_create_http_add_response_multiple_success(self):
        self.cmd_invoker.resource_check.return_value = [self.result['idle'], self.result['idle']]
        dict_successes = {self.result['success'].device_name:[self.result['success'],
                                                              self.result['success']]}
        ret = self.rmgr._create_http_add_response(dict_successes, {})
        expected = {self.result['success'].device_name:dict(return_code=200, status='idle')}
        self.assertEqual(expected, ret)

    def test_create_http_add_response_failure_bad_param_01(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response({}, create_dict_from_result(self.result['default']))
        expected = {self.result['default'].device_name:dict(return_code=400, status='invalid')}
        self._check_exception(cmgr.exception, 400, 'Could not add node(s).', expected)

    def test_create_http_add_response_failure_bad_param_02(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response({}, create_dict_from_result(self.result['bad_param']))
        expected = {self.result['bad_param'].device_name:dict(return_code=400,
                                                              status='invalid',
                                                              error='Invalid node_regex.')}
        self._check_exception(cmgr.exception, 400, 'Could not add node(s).', expected)

    def test_create_http_add_response_failure(self):
        self.cmd_invoker.resource_check.return_value = self.result['alloc']
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response({}, create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc')}
        self._check_exception(cmgr.exception, 404, 'Could not add node(s).', expected)

    def test_create_http_add_response_multiple_failures(self):
        dict_failures = deepcopy(create_dict_from_result(self.result['device']))
        dict_failures.update(create_dict_from_result(self.result['bad_param']))
        self.cmd_invoker.resource_check.return_value = [self.result['alloc'], self.result['default']]
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response({}, dict_failures)
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc'),
                    self.result['bad_param'].device_name:dict(return_code=400, status='invalid')}
        self._check_exception(cmgr.exception, 404, 'Could not add node(s).', expected)

    def test_create_http_add_response_multiple_failures_same_node(self):
        dict_failures = {self.result['device'].device_name:[self.result['device'],
                                                            self.result['device']]}
        dict_failures[self.result['device'].device_name][1].return_code = -1
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response({}, dict_failures)
        expected = {self.result['device'].device_name:dict(return_code=400, status='invalid')}
        self._check_exception(cmgr.exception, 400, 'Could not add node(s).', expected)

    def test_create_http_add_response_mixed(self):
        self.cmd_invoker.resource_check.return_value = [self.result['alloc'], self.result['idle']]
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response(create_dict_from_result(self.result['success']),
                                                create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:dict(return_code=404, status='alloc'),
                    self.result['success'].device_name:dict(return_code=200, status='idle')}
        self._check_exception(cmgr.exception, 207, 'Could not add some nodes.', expected)

    def test_create_http_add_plugin_not_installed(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.rmgr._create_http_add_response({}, \
                create_dict_from_result(self.result['plugin_not_installed']))
        self._check_exception(cmgr.exception, 424, 'Resource Manager plugin is not installed')
