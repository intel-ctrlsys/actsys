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

def split_command_results(results):
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


class Usage(object):
    """ Base class to manage usage messages for the REST API """

    def __init__(self):
        self._literals = dict(title='\n\t Control Rest API \n',
                              description="\n REST API for the Control System.\n ",
                              usage='\n Usage: \n',
                              http_method_supported='\tHTTP Method Supported: ',
                              http_method='GET|PUT\n\t',
                              url='http://<server>:<port>',
                              command='/<command>',
                              subcommand='/<subcommand>',
                              args_start='?',
                              args='<arg_1>=<value_1>,<arg_n>=<value_n>',
                              node_regex='node_regex=<regex>',
                              where='\n\n Where: \n',
                              server_desc="\t<server> is the server where the REST API is running. \n",
                              port_desc="\t<port> is the port where the REST API is listening.\n",
                              command_desc="\t<command> is the command to be excecuted by the control system.\n",
                              subcommand_desc="\t<subcommand> is the subcommand to be executed by the " \
                                              "control system. This might be optional.\n",
                              args_desc="\t<arg_1> and <arg_n> are arguments for that function, and " \
                                        "<value_1> and <value_n> are their corresponding values. These" \
                                        " might be optional.\n",
                              node_regex_desc="\t<regex> should be the name of a valid node identified by "\
                                              "its device_id, hostname, or IP address as stated in the " \
                                              "configuration file.\n"
                             )

    def get_usage_msg(self):
        """ Return usage message for REST API """
        return '{title}{description}{usage}{http_method_supported}{http_method}{url}{command}{subcommand}'\
               '{args_start}{args}{where}{server_desc}{port_desc}{command_desc}{subcommand_desc}'\
               '{args_desc}'.format(**self._literals)
