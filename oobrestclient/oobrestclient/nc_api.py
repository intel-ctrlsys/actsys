"""
Defines the user interface. Three APIs are exposed to user: get_value,
set_value, get_value_over_time
"""


import urllib
import requests


class ConnectError(Exception):
    """A connection error exception"""

    pass


class NodeController(object):
    """The NodeController class to allow users to read/write system values"""

    def __init__(self, host):
        self.host = host

    @staticmethod
    def get_response(url):
        try:
            return NodeController.verified_response(requests.get(url))
        except Exception as nc_exception:
            raise ConnectError(nc_exception.message)

    @staticmethod
    def post_response(url, json):
        try:
            response = requests.post(url, json=json)
            return NodeController.verified_response(response)
        except Exception as nc_exception:
            raise ConnectError(nc_exception.message)

    @staticmethod
    def verified_response(response):
        if response is None:
            raise ConnectError("response is None!")
        if response.status_code != 200:
            raise ConnectError("response status " + str(response.status_code))
        return response

    def url_with_route(self, path):
        return 'http://' + self.host + '/api/' + path

    def get_value(self, path):
        return NodeController.get_response(self.url_with_route(path)).json()

    def set_value(self, path, value):
        url = self.url_with_route(path)
        return NodeController.post_response(url, json=value).json()

    def get_value_over_time(self, path, duration, sample_rate):
        args = {'duration': duration, 'sample_rate': sample_rate}
        url = self.url_with_route(path) + '?' + urllib.urlencode(args)
        return NodeController.get_response(url).json()
