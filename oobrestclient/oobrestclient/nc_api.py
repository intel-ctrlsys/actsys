# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Defines the user interface. Three APIs are exposed to user: get_value,
set_value, get_value_over_time
"""

from urllib.parse import urlencode
import asyncio
import aiohttp


class ConnectError(Exception):
    """A connection error exception"""
    pass


class OobController(object):
    """The OobController class to allow users to read/write system values"""

    def __init__(self, host_list):
        self.loop = asyncio.get_event_loop()
        self.host_list = []
        for host in host_list:
            self.host_list.append(host)

    @staticmethod
    @asyncio.coroutine
    def _verified_response(method, *args, **kwargs):
        try:
            response = yield from method(*args, **kwargs)
        except Exception as nc_exception:
            return {"exception": "response status " + str(nc_exception)}
        try:
            if response.status != 200:
                return {"exception": "response status " + str(response.status)}
            json_content = yield from response.json()
            return json_content
        except Exception as nc_exception:
            response.close()
            return {"exception": str(nc_exception)}
        finally:
            yield from response.release()

    @staticmethod
    def _decode_response_to_dict(responses):
        return {key: value for d in responses for key, value in d.items()}

    def get_value(self, path):
        """
        Get the response from multiple servers asynchronously and send it to clients
        :param path:
        :return:
        """
        items = []
        with aiohttp.ClientSession(loop=self.loop) as session:
            for host in self.host_list:
                url = 'http://' + host + path
                item = OobController._verified_response(session.get, url)
                items.append(item)
            responses = self.loop.run_until_complete(asyncio.gather(*items))
        return OobController._decode_response_to_dict(responses)

    def set_value(self, path, value):
        """
        Set the value on multiple servers asynchronously and send response to clients
        :param path:
        :return:
        """
        items = []
        with aiohttp.ClientSession(loop=self.loop) as session:
            for host in self.host_list:
                url = 'http://' + host + path
                item = OobController._verified_response(session.post, url, json=value)
                items.append(item)
            responses = self.loop.run_until_complete(asyncio.gather(*items))
        return OobController._decode_response_to_dict(responses)

    def get_value_over_time(self, path, duration, sample_rate):
        """
        Get the response from multiple servers asynchronously and send it to clients
        :param path:
        :return:
        """
        items = []
        args = {'duration': duration, 'sample_rate': sample_rate}
        with aiohttp.ClientSession(loop=self.loop) as session:
            for host in self.host_list:
                url = 'http://' + host + path + '?' + urlencode(args)
                item = OobController._verified_response(session.get, url)
                items.append(item)
            responses = self.loop.run_until_complete(asyncio.gather(*items))
        return OobController._decode_response_to_dict(responses)
