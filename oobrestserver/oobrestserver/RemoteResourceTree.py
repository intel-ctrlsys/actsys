# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""Remote access to resource trees hosted by other server instances"""

import requests
from oobrestserver.BaseResourceTree import BaseResourceTree


class RemoteResourceTree(BaseResourceTree):
    """Implements the BaseResourceTree contract by issuing HTTP requests to other servers."""

    def __init__(self, remote_host):
        self.url = remote_host

    def list_children(self, recursive=False):
        response = requests.get(self.url, params={'recursive': 1})
        return response.json()['']['samples'][0]

    def get_method(self, label):
        if label == '#getter':
            def get_request(**kwargs):
                return requests.get(self.url, params=kwargs)
            return get_request
        if label == '#setter':
            def post_request(value, **kwargs):
                return requests.post(self.url, json=value, params=kwargs)
            return post_request
        raise RuntimeError('Method not supported')

    def add_resources(self, config):
        return requests.put(self.url, data=config)

    def remove_resources(self, child):
        return requests.delete(self.url+'/'+child)

    def dispatch(self, vpath):
        return [RemoteResourceTree(self.url+'/'+'/'.join(vpath))]
