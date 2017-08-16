# -*- coding: utf-8 -*-
"""Defines a route dispatcher for parallel operations.

This module defines the ParallelDispatcher, which is a special dispatcher that
handles ambiguous URL routes in parallel.

Typically URL route dispatchers (objects with the _cp_dispatch method) will call
the dispatch method to find the next dispatcher, and so on, until the final node
provides the HTTP method being requested.

The ParallelDispatcher object pretends to be a traditional dispatcher, but will
instead, upon initialization, save the URL route. Then, when _cp_dispatch is
called, it will delete the route passed as an argument, and return itself.

Then, the request will invoke the appropriate HTTP method on the
ParallelDispatcher. The provided HTTP methods will take the previously-stored
(ambiguous) route, and resolve it to all matching routes provided by the server.

The appropriate method for every matching route are be executed in parallel,
and the results are aggregated and returned.

"""

import re
import functools
from multiprocessing import Process
from multiprocessing.queues import SimpleQueue

import cherrypy


class ParallelDispatcher(object):
    """Dispatcher for ambiguous URLs that identify multiple resources."""

    exposed = True

    def __init__(self, dispatcher, vpath):
        """Store the ambiguous route and determine all matches."""
        self.dispatcher = dispatcher
        urls = self.dispatcher.ls_from('', leaves_only=True)
        glob = '/'.join(vpath)
        regex = ParallelDispatcher.regex_from_glob(glob)
        self.matching_urls = [x for x in urls if re.match(regex, x)]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, **kwargs):
        return self.aggregate('get', **kwargs)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        return self.aggregate('set', value=cherrypy.request.json)

    def _cp_dispatch(self, vpath):
        del vpath[:]
        return self

    def aggregate(self, method, **kwargs):
        """Call method on all requested dispatchers, aggregating the results."""
        processes = {}
        for url in self.matching_urls:
            result_queue = SimpleQueue()
            func = getattr(self.dispatcher_at(url), method)
            bound = functools.partial(ParallelDispatcher.append_func_result,
                                      result_queue, func, **kwargs)
            process = Process(target=bound)
            processes[process] = result_queue
            process.start()
        aggregate_answer = {}
        for process in processes:
            process.join()
            result_queue = processes[process]
            aggregate_answer.update(result_queue.get())
        return aggregate_answer

    @staticmethod
    def append_func_result(shared_results, func, **kwargs):
        try:
            shared_results.put(func(**kwargs))
        except Exception as plugin_exception:
            print str(plugin_exception)

    def dispatcher_at(self, url):
        """Find the DispatchNode for the given URL."""
        if not url:
            return self.dispatcher
        vpath = url.split('/')
        dispatcher = self.dispatcher
        while vpath:
            dispatcher = dispatcher._cp_dispatch(vpath)
        return dispatcher

    @staticmethod
    def regex_from_glob(pattern):
        """Method to convert URL globstar patterns to Python regexes"""

        state = 'start'
        result = ''
        bracket_set = ''
        bracket_negate = False

        for symbol in pattern:
            if state == 'start':
                if symbol == '*':
                    state = '*'
                elif symbol == '?':
                    result += '.'
                elif symbol == '[':
                    bracket_negate = False
                    state = '['
                else:
                    result += symbol
            elif state == '*':
                if symbol == '*':
                    result += '.*'
                    state = 'start'
                else:
                    result += '[^/]*' + symbol
                    state = 'start'
            elif state == '[':
                if symbol == '!':
                    bracket_negate = True
                elif symbol == ']':
                    if bracket_negate:
                        result += '[^' + bracket_set + ']'
                    else:
                        result += '[' + bracket_set + ']'
                    state = 'start'
                else:
                    bracket_set += symbol
        if state == '*':
            result += '[^/]*'
        elif state == '[':
            message = 'Invalid glob expression: open bracket not closed'
            raise cherrypy.HTTPError(status=400, message=message)
        result += '$'
        return result
