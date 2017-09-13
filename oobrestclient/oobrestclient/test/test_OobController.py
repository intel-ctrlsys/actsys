# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
from unittest import TestCase
from aioresponses import aioresponses
from aiohttp import ClientHttpProxyError
from ..nc_api import OobController


class TestOobController(TestCase):

    class FakeBadResponse(object):
        def __init__(self):
            self.status_code = 300

    class FakeGoodResponse(object):
        def __init__(self):
            self.status_code = 200
            self.json = lambda: "A perfectly good response"

    @staticmethod
    def raise_ex(ex):
        raise ex

    def setUp(self):
        self.nc = OobController(['localhost/'])

    @aioresponses()
    def test_get_value_bad_response(self, mocked):
        mocked.get('http://localhost/hello_url', status=404)
        response = self.nc.get_value('hello_url')
        self.assertEqual(response, {'exception': 'response status 404'})

    @aioresponses()
    def test_get_value_http_exception(self, mocked):
        mocked.get('http://localhost/hello_url', exception=ClientHttpProxyError(request_info="", history=""))
        response = self.nc.get_value('hello_url')
        self.assertEqual(response, {'exception': "response status 0, message=''"})

    @aioresponses()
    def test_get_value_good_response(self, mocked):
        mocked.get('http://localhost/hello_url', status=200,  payload=dict(foo='A perfectly good response'))
        response = self.nc.get_value('hello_url')
        self.assertEqual(response, {"foo": "A perfectly good response"})

    @aioresponses()
    def test_set_value(self, mocked):
        mocked.post('http://localhost/hello_url', status=200, payload=dict(foo='A perfectly good response'))
        response = self.nc.set_value('hello_url', 'some_value')
        self.assertEqual(response, {"foo": "A perfectly good response"})

    @aioresponses()
    def test_get_value_good_response_over_time(self, mocked):
        mocked.get('http://localhost/hello_url?sample_rate=1&duration=10', status=200,
                   payload=dict(foo='A perfectly good response'))
        response = self.nc.get_value_over_time('hello_url', 10, 1)
        self.assertEqual(response, {"foo": "A perfectly good response"})
