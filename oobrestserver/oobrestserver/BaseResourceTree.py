# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
import oobrestserver.GlobTools as GlobTools

class BaseResourceTree(object):

    def list_children(self, recursive=False): # pragma: no cover
        raise NotImplementedError()

    def get_method(self, label): # pragma: no cover
        raise NotImplementedError()

    def add_resources(self, config): # pragma: no cover
        raise NotImplementedError()

    def remove_resources(self, child): # pragma: no cover
        raise NotImplementedError()

    def cleanup(self): # pragma: no cover
        pass

    def dispatch(self, vpath): # pragma: no cover
        raise NotImplementedError()

    def _globstar_dispatch(self, vpath):
        return [node for node in self.list_children(True) if GlobTools.glob_match(node.route, '/'.join(vpath))]
