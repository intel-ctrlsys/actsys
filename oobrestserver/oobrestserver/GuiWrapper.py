# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""Sample of a GUI page generator to demonstrate the ease of adding a GUI."""


import json
import cherrypy


class GuiWrapper(object):
    """Wraps the data from the provider api in an HTML page."""

    exposed = True

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.vpath = []

    def _cp_dispatch(self, vpath):
        self.vpath = vpath[:]
        del vpath[:]
        return self

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **kwargs):
        dispatcher = self.dispatcher
        while self.vpath:
            dispatcher = dispatcher._cp_dispatch(self.vpath)
        document = "<pre>" + json.dumps(dispatcher.GET(**kwargs), indent=4) + '</pre>'
        return document
