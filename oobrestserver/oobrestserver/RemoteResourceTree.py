# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

import requests

from oobrestserver.BaseResourceTree import BaseResourceTree
from oobrestserver import GlobTools

class RemoteResourceTree(BaseResourceTree):

    def __init__(self, remote_host):
        self.url = remote_host

    def list_children(self, recursive=False):
        # parse result of GET @ url?recursive=1
        # requests.get()
        return []

    def get_method(self, label):
        if label == '#getter':

            pass # wrap GET requests w/ URL params <-> kwargs mapped. Return a function!l
        if label == '#setter':
            pass # wrap POST like GET above
        raise NotImplementedError()

    def add_resources(self, config):
        raise NotImplementedError() # wrap PUT after server supports this

    def remove_resources(self, child):
        raise NotImplementedError() # wrap DELETE after server supports this

    def cleanup(self):
        pass # that's really all there is to it.

    def dispatch(self, vpath):
        if not vpath:
            return [self]
        return [node for node in self.list_children(True) if GlobTools.glob_match(node.route, '/'.join(vpath))]
