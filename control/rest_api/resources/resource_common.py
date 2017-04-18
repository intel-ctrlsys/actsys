# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Base class for endpoint managers """
from abc import abstractmethod
from flask_restful import Resource
from flask import jsonify, make_response, request

from ...cli.command_invoker import CommandInvoker
from ..utils.utils import print_msg, Usage

class HTTP(object):
    """ Container for HTTP return codes """
    STATUS_OK = 200
    MULTI_STATUS = 207
    BAD_REQUEST = 400
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    FAILED_DEPENDENCY = 424
    NOT_IMPLEMENTED = 501

class ResourceCommon(Resource):
    """ Common Resource Class """

    def __init__(self, cmd_invoker=None, debug=False):
        super(ResourceCommon, self).__init__()
        self.cmd_invoker = cmd_invoker if isinstance(cmd_invoker, CommandInvoker) else None
        self.debug = debug
        self.usage = Usage()

    @classmethod
    def _raise_if_is_single_failure(cls, response, message=""):
        """ Raise ResourceCommonException if there's only one failure. """
        if len(response.keys()) == 1:
            item = response.itervalues().next()
            raise ResourceCommonException(item['return_code'], message, response)

    @classmethod
    def _raise_all_failed(cls, response, message="", error_code=HTTP.NOT_FOUND):
        """ Raise ResourceCommonException, as all the commands failed. """
        raise ResourceCommonException(error_code, message, response)

    @classmethod
    def _raise_if_is_none(cls, value, message="", error_code=HTTP.CONFLICT):
        """ Raise ResourceCommonException if the parameter is None. """
        if value is None:
            raise ResourceCommonException(error_code, message)

    @classmethod
    def _raise_if_is_empty(cls, param, message="", error_code=HTTP.CONFLICT):
        """ Raise ResourceCommonException if the parameter is None or empty. """
        if not param:
            raise ResourceCommonException(error_code, message)


    def _debug_msg(self, message):
        if self.debug:
            print_msg(self.__class__.__name__, message)

    def _invalid_method_response(self, method, subcommand):
        usage_dict = dict(usage=self.usage.get_subcommand_usage_msg(subcommand))
        return self._create_response(HTTP.METHOD_NOT_ALLOWED,
                                     method + ' method not allowed for ' + subcommand + ' option.',
                                     usage_dict)

    def _raise_if_no_cmd_invoker(self):
        """ Raise ResourceManagerException if there's no command invoker available"""
        if not self.cmd_invoker:
            raise ResourceCommonException(HTTP.CONFLICT, 'No CommandInvoker available.')

    def _create_http_response_(self, subcommand, successes, failures):
        self._raise_if_is_none(successes, 'Could not parse command results.')
        self._raise_if_is_none(failures, 'Could not parse command results.')
        response = dict()
        self._fill_response_from_successes(response, successes)
        self._fill_response_from_failures(response, failures)
        self._raise_if_is_empty(response, 'Could not parse command results.')
        if successes and not failures:
            return response
        if failures and not successes:
            self._raise_if_is_single_failure(response, 'Could not ' + subcommand + ' node(s).')
            self._raise_all_failed(response, 'Could not ' + subcommand + ' node(s).')
        raise ResourceCommonException(HTTP.MULTI_STATUS,
                                      'Could not ' + subcommand + ' some nodes.', response)

    @abstractmethod
    def _fill_response_from_successes(self, response, successes):
        self._raise_not_implemented("_fill_response_from_successes")

    @abstractmethod
    def _fill_response_from_failures(self, response, failures):
        self._raise_not_implemented("_fill_response_from_failures")

    @classmethod
    def _raise_not_implemented(cls, method_name=''):
        raise ResourceCommonException(HTTP.NOT_IMPLEMENTED,
                                      "Missing implementation of the method {}".format(method_name))

    @classmethod
    def _create_response_from_exception(cls, exception):
        """ Creates Flask response from a ResourceCommonException """
        return cls._create_response(getattr(exception, 'error_code', HTTP.NOT_FOUND),
                                    getattr(exception, 'message', ""),
                                    getattr(exception, 'response', None))

    @classmethod
    def _create_response(cls, error_code, message="", data=None):
        if not data:
            return make_response(message+'\n', error_code)
        data['message'] = message
        return make_response(jsonify(data), error_code)

    def dispatch_requests(self, valid_subcommands, subcommand=None, method='GET'):
        """ Method to handle HTTP Requests """
        self._debug_msg('subcommand: {} args: {}'.format(subcommand, request.values))

        if subcommand is None:
            return self._create_response(HTTP.BAD_REQUEST, 'Invalid subcommand (no subcommand)',
                                         dict(usage=self.usage.get_default_usage_msg()))

        if subcommand not in valid_subcommands:
            return self._create_response(HTTP.BAD_REQUEST,
                                         'Invalid subcommand: {0}'.format(subcommand),
                                         dict(usage=self.usage.get_default_usage_msg()))

        local_function = getattr(self, '_{}_{}_subcommand'.format(method.lower(), subcommand), None)

        if local_function:
            return local_function(subcommand, **dict(request.values.items()))

        return self._invalid_method_response(method.upper(), subcommand)


class ResourceCommonException(Exception):
    """ Class to raise Errors """
    def __init__(self, error_code=HTTP.NOT_FOUND, message="", response=None):
        super(self.__class__, self).__init__(super)
        self.error_code = error_code
        self.message = message
        self.response = response
