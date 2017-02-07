# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
This module defines some utility functions.
"""
from __future__ import print_function
from ...commands import CommandResult

def append_to_list_in_dictionary(dictionary, result):
    """ Takes a CommandResult and appends it to a list under device_name
        in the provided dictionary """
    if dictionary is None or not isinstance(dictionary, dict) or \
        result is None or not isinstance(result, CommandResult):
        return -1
    value = dictionary.get(result.device_name)
    if value is None:
        dictionary[result.device_name] = result
    elif isinstance(value, list):
        dictionary[result.device_name].append(result)
    else:
        dictionary[result.device_name] = [value]
        dictionary[result.device_name].append(result)
    return 0

def handle_command_results(results):
    """ Receives a list of CommandResult objects and split it into two dictionaries:
        success - for all the successful results ordered by device_name.
        fail - for all the failing results ordered by device_name. """
    success = dict()
    fail = dict()
    if results:
        if isinstance(results, list):
            for result in results:
                if isinstance(result, CommandResult):
                    if result.return_code != 0:
                        append_to_list_in_dictionary(fail, result)
                    else:
                        append_to_list_in_dictionary(success, result)
        elif isinstance(results, CommandResult):
            if results.return_code != 0:
                append_to_list_in_dictionary(fail, results)
            else:
                append_to_list_in_dictionary(success, results)
    return success, fail


def print_msg(class_name, message):
    """ Formatted print """
    if not class_name:
        class_name = "REST API"
    print (" * {0} - {1}".format(class_name, message))
