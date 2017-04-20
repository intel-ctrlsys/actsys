# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module to handle Bios related requests """
from flask import jsonify

from ..utils.utils import split_command_results, Usage
from ...plugin.manager import PluginManagerException

from .resource_common import ResourceCommon, ResourceCommonException

class Bios(ResourceCommon):
    """ Bios Resource Class """

    def __init__(self, cmd_invoker=None, debug=False):
        super(Bios, self).__init__(cmd_invoker, debug)
        self.usage = BiosUsage()
        self.valid_commands = ['update']

    def _put_update_subcommand(self, subcommand, **kwargs):
        return self._handle_subcommand(self._create_http_update_response, self._update_bios, subcommand, **kwargs)

    def _update_bios(self, **kwargs):
        node_regex = kwargs.get('node_regex', '')
        image = kwargs.get('image', '')
        self._raise_if_no_cmd_invoker()
        self._raise_if_is_empty(node_regex, 'node_regex parameter was not provided.', 400)
        self._raise_if_is_empty(image, 'image parameter was not provided.', 400)
        return self.cmd_invoker.bios_update(node_regex, image)

    def _create_http_update_response(self, successes, failures):
        return self._create_http_response_('update', successes, failures)

    def _fill_response_from_successes(self, response, successes):
        for node in successes:
            response[node] = dict(return_code=200,
                                  message=successes[node].message)

    def _fill_response_from_failures(self, response, failures):
        for node in failures:
            if not isinstance(failures[node], list):
                response[node] = dict(return_code=404, error=failures[node].message)
            else:
                for fail in failures[node]:
                    response[node] = dict(return_code=404, error=fail.message)

    def _handle_subcommand(self, response_fn, subcommand_fn, subcommand, **kwargs):
        try:
            success, fail = split_command_results(subcommand_fn(**kwargs))
            return jsonify(response_fn(success, fail))
        except ResourceCommonException as rme:
            self._add_usage_message(subcommand, rme)
            return self._create_response_from_exception(rme)
        except PluginManagerException as pme:
            rme = ResourceCommonException(424,
                                          'Bios plugin is not installed. \n'
                                          + pme.message)
            return self._create_response_from_exception(rme)

    def _add_usage_message(self, subcommand, exception):
        if exception.error_code == 400:
            if exception.response is None:
                exception.response = dict(usage=self.usage.get_subcommand_usage_msg(subcommand))
            if isinstance(exception.response, dict):
                exception.response['usage'] = self.usage.get_subcommand_usage_msg(subcommand)

    def get(self, subcommand=None):
        """ Handles HTTP GET requests"""
        return self.dispatch_requests(self.valid_commands, subcommand, 'get')

    def put(self, subcommand=None):
        """ Handles HTTP PUT requests"""
        return self.dispatch_requests(self.valid_commands, subcommand, 'put')

class BiosUsage(Usage):
    """ Class to manage usage messages for the Bios """

    def __init__(self):
        super(BiosUsage, self).__init__()
        self._update = '/update'
        self._put = 'PUT'
        self._get = 'GET'
        self._subcommand = self._literals['subcommand']
        self._subcommand_desc = "\t<subcommand> could be 'update' (PUT), " + \
                                "options.\n"
        self._set_default_values()

    def _set_default_values(self):
        self._literals['command'] = '/bios'
        self._literals['command_desc'] = ''
        self._literals['args'] = self._literals['node_regex'] + '&image=<image_file_path>'
        image_desc = '\t<image_file_path> is the path of the bios image to be used. \n'
        self._literals['args_desc'] = self._literals['node_regex_desc'] + image_desc

    def _create_subcommand_usage_msg(self, subcommand, http_method, subcommand_desc=''):
        self._literals['subcommand'] = subcommand
        self._literals['http_method'] = http_method+'\n\t'
        self._literals['subcommand_desc'] = subcommand_desc
        return self.get_usage_msg()

    def _get_update_usage_msg(self):
        """ Return usage message for 'update' subcommand"""
        self._literals['description'] = "\n Updates bios image of given node(s).\n"
        return self._create_subcommand_usage_msg(self._update, self._put)

    def get_default_usage_msg(self):
        """ Return usage message for bios. """
        self._literals['description'] = "\n Bios command.\n"
        return self._create_subcommand_usage_msg(self._subcommand,
                                                 self._get + '|' + self._put, self._subcommand_desc)
