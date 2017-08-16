# -*- coding: utf-8 -*-
"""Sample of a GUI page generator to demonstrate the ease of adding a GUI."""

import json

import cherrypy


class GuiDispatcher(object):
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
    def GET(self):
        """Find the dispatcher you want, get it's GET data, and pretty-print"""
        if not self.vpath:
            return "welcome to the gui pages"
        dispatcher = self.dispatcher
        while self.vpath:
            dispatcher = dispatcher._cp_dispatch(self.vpath)
        document = "<pre>" + json.dumps(dispatcher.GET(), indent=4) + '</pre>'
        return document
