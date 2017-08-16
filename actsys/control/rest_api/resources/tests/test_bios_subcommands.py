# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing Bios """
from __future__ import print_function
from copy import deepcopy
from ..resource_common import ResourceCommonException
from .test_bios import TestBiosBase, create_dict_from_result

class TestBiosUpdate(TestBiosBase):
    """ Class to test update related functions """

    def test_update_bios_no_command_invoker(self):
        with self.assertRaises(ResourceCommonException)as cmgr:
            self.bios_defaults._update_bios(node_regex=self.node_regex['single'],
                                            image=self.image['valid'])
        self._check_exception(cmgr.exception, 409, 'No CommandInvoker available.')

    def test_update_bios(self):
        self.cmd_invoker.bios_update.return_value = self.result['success']
        ret = self.bios._update_bios(node_regex=self.result['success'].device_name,
                                     image=self.image['valid'])
        self._check_result(ret, self.result['success'].return_code,
                           self.result['success'].message)

    def test_create_http_update_response_none_dictionaries(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.bios._create_http_update_response(None, None)
        self._check_exception(cmgr.exception, 409, 'Could not parse command results.', None, False)

    def test_create_http_update_response_empty_dictionaries(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.bios._create_http_update_response({}, {})
        self._check_exception(cmgr.exception, 409, 'Could not parse command results.', None, False)

    def test_create_http_update_response_single_success(self):
        self.cmd_invoker.bios_update.return_value = self.result['success']
        success = create_dict_from_result(self.result['success'])
        ret = self.bios._create_http_update_response(success, {})
        expected = {self.result['success'].device_name:self.http_dict['success']}
        self.assertEqual(expected, ret)

    def test_create_http_update_response_multiple_success(self):
        self.cmd_invoker.bios_update.return_value = [self.result['success'], self.result['success_other']]
        dict_successes = {self.result['success'].device_name:self.result['success'],
                          self.result['success_other'].device_name:self.result['success_other']
                         }
        ret = self.bios._create_http_update_response(dict_successes, {})
        expected = {self.result['success'].device_name:self.http_dict['success'],
                    self.result['success_other'].device_name:self.http_dict['success_other']
                   }
        self.assertEqual(expected, ret)

    def test_create_http_update_response_failure_bad_param(self):
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.bios._create_http_update_response({}, create_dict_from_result(self.result['bad_param']))
        expected = {self.result['bad_param'].device_name:self.http_dict['bad_param']}
        self._check_exception(cmgr.exception, 404, 'Could not update node(s).', expected)

    def test_create_http_update_response_failure(self):
        self.cmd_invoker.bios_update.return_value = self.result['device']
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.bios._create_http_update_response({}, create_dict_from_result(self.result['device']))
        expected = {self.result['device'].device_name:self.http_dict['device']}
        self._check_exception(cmgr.exception, 404, 'Could not update node(s).', expected)

    def test_create_http_update_response_multiple_failures(self):
        dict_failures = deepcopy(create_dict_from_result(self.result['device']))
        dict_failures.update(create_dict_from_result(self.result['bad_param']))
        self.cmd_invoker.bios_update.return_value = [self.result['device'], self.result['bad_param']]
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.bios._create_http_update_response({}, dict_failures)
        expected = {self.result['device'].device_name:self.http_dict['device'],
                    self.result['bad_param'].device_name:self.http_dict['bad_param']
                   }
        self._check_exception(cmgr.exception, 404, 'Could not update node(s).', expected)

    def test_create_http_update_response_multiple_failures_same_node(self):
        dict_failures = {self.result['device'].device_name:[self.result['device'],
                                                            self.result['device']]}
        dict_failures[self.result['device'].device_name][1].return_code = 1
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.bios._create_http_update_response({}, dict_failures)
        expected = {self.result['device'].device_name:self.http_dict['device']}
        self._check_exception(cmgr.exception, 404, 'Could not update node(s).', expected)

    def test_create_http_update_response_mixed(self):
        self.cmd_invoker.bios_update.return_value = [self.result['success'], self.result['bad_param']]
        with self.assertRaises(ResourceCommonException) as cmgr:
            self.bios._create_http_update_response(create_dict_from_result(self.result['success']),
                                                   create_dict_from_result(self.result['bad_param']))
        expected = {self.result['bad_param'].device_name:self.http_dict['bad_param'],
                    self.result['success'].device_name:self.http_dict['success']
                   }
        self._check_exception(cmgr.exception, 207, 'Could not update some nodes.', expected)
