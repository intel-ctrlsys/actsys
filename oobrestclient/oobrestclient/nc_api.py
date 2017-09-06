"""
Defines the user interface. Three APIs are exposed to user: get_value,
set_value, get_value_over_time
"""

from urllib.parse import urlencode
import requests


class ConnectError(Exception):
    """A connection error exception"""
    pass


class NodeController(object):
    """The NodeController class to allow users to read/write system values"""

    def __init__(self, host):
        self.base_url = 'http://' + host + '/api/'

    @staticmethod
    def verified_response(method, *args, **kwargs):
        try:
            response = method(*args, **kwargs)
        except Exception as nc_exception:
            raise ConnectError(str(nc_exception))
        if response is None:
            raise ConnectError("response is None!")
        if response.status_code != 200:
            raise ConnectError("response status " + str(response.status_code))
        return response.json()

    def get_value(self, path):
        url = self.base_url + path
        return NodeController.verified_response(requests.get, url)

    def set_value(self, path, value):
        url = self.base_url + path
        return NodeController.verified_response(requests.post, url, json=value)

    def get_value_over_time(self, path, duration, sample_rate):
        args = {'duration': duration, 'sample_rate': sample_rate}
        url = self.base_url + path + '?' + urlencode(args)
        return NodeController.verified_response(requests.get, url)
