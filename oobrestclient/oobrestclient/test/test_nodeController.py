from unittest import TestCase
from ..nc_api import NodeController
from ..nc_api import ConnectError

import requests

class TestNodeController(TestCase):

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
        self.nc = NodeController('localhost')

    def check_connect_error(self):
        try:
            self.nc.get_value('hello_url')
        except ConnectError:
            return
        self.fail()

    def test_get_value_none(self):
        requests.get = lambda url: None
        self.check_connect_error()

    def test_get_value_throws(self):
        requests.get = lambda url: TestNodeController.raise_ex(AssertionError('testing'))
        self.check_connect_error()

    def test_get_value_bad(self):
        requests.get = lambda url: TestNodeController.FakeBadResponse()
        self.check_connect_error()

    def test_get_value(self):
        requests.get = lambda url: TestNodeController.FakeGoodResponse()
        response = self.nc.get_value('hello_url')
        self.assertEqual(response, "A perfectly good response")

    def test_set_value(self):
        requests.post = lambda url, json: TestNodeController.FakeGoodResponse()
        response = self.nc.set_value('hello_url', 'some_value')
        self.assertEqual(response, "A perfectly good response")

    def test_get_value_over_time(self):
        requests.get = lambda url: TestNodeController.FakeGoodResponse()
        response = self.nc.get_value_over_time('hello_url', 10, 1)
        self.assertEqual(response, "A perfectly good response")
