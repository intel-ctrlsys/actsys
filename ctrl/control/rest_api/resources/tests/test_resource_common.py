# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing ResourceManager """
from unittest import TestCase
from ..resource_common import ResourceCommonException
from ..resource_common import ResourceCommon, HTTP


class TestResourceCommon(TestCase):
    """ Class for Resource Common Class Testing """
    def setUp(self):
        self.resource = ResourceCommon()

    def _check_exception(self, exception, exp_error_code, exp_message, exp_response=None):
        self.assertEqual(exp_error_code, exception.error_code)
        self.assertIn(exp_message, exception.message)
        self.assertEqual(exception.response, exp_response)

    def _test_abstract_method(self, method_name, function):
        with self.assertRaises(ResourceCommonException) as rce:
            function(None, None)
            self._check_exception(rce.exception,
                                  HTTP.NOT_IMPLEMENTED,
                                  "Missing implementation of the method {}".format(method_name))

    def test_fill_response_from_successes(self):
        self._test_abstract_method('_fill_response_from_successes',
                                   self.resource._fill_response_from_successes)

    def test_fill_response_from_failures(self):
        self._test_abstract_method('_fill_response_from_failures',
                                   self.resource._fill_response_from_failures)


