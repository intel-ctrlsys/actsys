# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing Utils """

from unittest import TestCase
from copy import deepcopy
from mock import patch, call
from ..utils import handle_command_results, print_msg, \
                    append_to_list_in_dictionary
from ....commands import CommandResult

def mock_print_and_test(class_name, msg, exp_class_name, exp_msg):
    """ Mocks the builtin print function and checks for a given message """
    with patch('__builtin__.print') as mock_print:
        print_msg(class_name, msg)
        mock_print.assert_has_calls(
            [
                call(' * {0} - {1}'.format(exp_class_name, exp_msg))
            ]
        )

class TestUtils(TestCase):
    """Class to test utils's functions. """
    def setUp(self):
        self.node = 'node0'
        self.msg = "Some message."
        self.default_class_name = "REST API"
        self.result = CommandResult()
        self.base_none_dic = {self.result.device_name: self.result}
        self.result_device = CommandResult(device_name=self.node)
        self.base_dic = {self.result_device.device_name: self.result_device}
        self.result_success = CommandResult(0, "Success")
        self.base_success_dic = {self.result_success.device_name: self.result_success}

    def test_print_msg_no_class_no_msg(self):
        """ Tests print_msg without class_name nor message"""
        mock_print_and_test(None, None, self.default_class_name, None)

    def test_print_msg(self):
        """ Tests print_msg function """
        mock_print_and_test(self.__class__, self.msg, self.__class__, self.msg)

    def test_append_to_list_in_dictionary_None_values(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = None
        self.assertEqual(-1, append_to_list_in_dictionary(mydic, None))
        self.assertIsNone(mydic)

    def test_append_to_list_in_dictionary_invalid_types(self):
        """ Tests the append_to_list_in_dictionary function """
        self.assertEqual(-1, append_to_list_in_dictionary(self.msg, self.msg))

    def test_append_to_list_in_dictionary_first_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result))
        self.assertEqual(self.base_none_dic, mydic)

    def test_append_to_list_in_dictionary_second_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = deepcopy(self.base_none_dic)
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result))
        expected = {self.result.device_name: [self.result, self.result]}
        self.assertEqual(expected, mydic)

    def test_append_to_list_in_dictionary_third_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {self.result.device_name: [self.result, self.result]}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result))
        expected = {self.result.device_name: [self.result, self.result, self.result]}
        self.assertEqual(expected, mydic)

    def test_append_to_list_in_dictionary_first_device_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result_device))
        self.assertEqual(self.base_dic, mydic)

    def test_append_to_list_in_dictionary_second_device_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = deepcopy(self.base_dic)
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result_device))
        expected = {self.result_device.device_name:[self.result_device,
                                                    self.result_device]}
        self.assertEqual(expected, mydic)

    def test_append_to_list_in_dictionary_third_device_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {self.result_device.device_name:[self.result_device,
                                                 self.result_device]}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result_device))
        expected = {self.result_device.device_name:[self.result_device,
                                                    self.result_device,
                                                    self.result_device]}
        self.assertEqual(expected, mydic)

    def test_handle_command_None_results(self):
        """ Tests the handle_command_results function """
        success, fail = handle_command_results(None)
        self.assertEqual(success, fail)
        self.assertFalse(success)

    def test_handle_command_empty_results(self):
        """ Tests the handle_command_results function """
        success, fail = handle_command_results(list())
        self.assertEqual(success, fail)
        self.assertFalse(success)

    def test_handle_command_invalid_result(self):
        """ Tests the handle_command_results function """
        success, fail = handle_command_results(self.msg)
        self.assertEqual(success, fail)
        self.assertFalse(success)

    def test_handle_command_single_result(self):
        """ Tests the handle_command_results function """
        success, fail = handle_command_results(self.result)
        self.assertFalse(success)
        self.assertEqual(self.base_none_dic, fail)

    def test_handle_command_multiple_results(self):
        """ Tests the handle_command_results function """
        results = [self.result, self.result]
        success, fail = handle_command_results(results)
        self.assertFalse(success)
        self.assertEqual({self.result.device_name:results}, fail)

    def test_handle_command_single_result_success(self):
        """ Tests the handle_command_results function """
        success, fail = handle_command_results(self.result_success)
        self.assertFalse(fail)
        self.assertEqual(self.base_success_dic, success)

    def test_handle_command_multiple_results_success(self):
        """ Tests the handle_command_results function """
        results = [self.result_success, self.result_success]
        success, fail = handle_command_results(results)
        self.assertFalse(fail)
        self.assertEqual({self.result_success.device_name:results}, success)

    def test_handle_command_multiple_results_both(self):
        """ Tests the handle_command_results function """
        results = [self.result, self.result_success]
        success, fail = handle_command_results(results)
        self.assertEqual(self.base_none_dic, fail)
        self.assertEqual(self.base_success_dic, success)

    def test_handle_command_multiple_results_invalid(self):
        """ Tests the handle_command_results function """
        results = [self.msg, self.result_success]
        success, fail = handle_command_results(results)
        self.assertFalse(fail)
        self.assertEqual(self.base_success_dic, success)