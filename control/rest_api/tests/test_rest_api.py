# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing ControlRestApi """
from unittest import TestCase
from mock import patch
from ..rest_api import ControlRestApi

def create_flags_dict(dfx, debug):
    """ Creates a dictionary for the ControlRestApi flags """
    return dict(dfx=dfx, debug=debug)

class TestControlRestApi(TestCase):
    """ Class for testing ControlRestApi """
    def setUp(self):
        self.rest_api = ControlRestApi(flags=create_flags_dict(True, True))
        self.rest_api.flask_app.config['TESTING'] = True
        self.test_app = self.rest_api.flask_app.test_client()

    def test__load_config__(self):
        """ Test for __load_config__ function """
        self.assertTrue(self.rest_api.flask_app.config['TESTING'])

    def test_init__defaults(self):
        """ Tests init function with default values """
        rest_api = ControlRestApi()
        self.assertIsNotNone(rest_api)
        self.assertFalse(rest_api.dfx)
        self.assertFalse(rest_api.debug)
        self.assertFalse(rest_api.dfx_resource_mgr)

    def test__init__dfx_and_debug_enabled(self):
        """ Tests init function with debug and dfx enabled """
        rest_api = ControlRestApi(flags=create_flags_dict(True, True))
        self.assertIsNotNone(rest_api)
        self.assertTrue(rest_api.dfx)
        self.assertTrue(rest_api.debug)
        self.assertTrue(rest_api.dfx_resource_mgr)

    def test__init__no_dfx_with_dfx_data(self):
        """ Tests init function with global dfx disabled but enabled for resource_mgr """
        dfx_data = {'resource_mgr':True}
        rest_api = ControlRestApi(dfx_data=dfx_data)
        self.assertIsNotNone(rest_api)
        self.assertFalse(rest_api.dfx)
        self.assertTrue(rest_api.dfx_resource_mgr)

    def test__init__dfx_with_dfx_data(self):
        """ Tests init function with global dfx enabled but disabled for resource_mgr """
        dfx_data = {'resource_mgr':False}
        rest_api = ControlRestApi(flags=dict(dfx=True), dfx_data=dfx_data)
        self.assertIsNotNone(rest_api)
        self.assertTrue(rest_api.dfx)
        self.assertFalse(rest_api.dfx_resource_mgr)

    def test__init__no_dfx_invalid_dfx_data(self):
        """ Tests init function with global dfx disabled and invalid dfx_data """
        dfx_data = {'foo':True}
        rest_api = ControlRestApi(dfx_data=dfx_data)
        self.assertIsNotNone(rest_api)
        self.assertFalse(rest_api.dfx)
        self.assertFalse(rest_api.dfx_resource_mgr)

    def test_run(self):
        """ Tests run function """
        with patch.object(self.rest_api.flask_app, 'run') as mock_run:
            self.rest_api.run()
            mock_run.assert_called_once()
            mock_run.assert_called_with(debug=True, host=None, port=None)
