# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Contains the ResponseBuilder class, which represents the service of one request
"""

import functools
import threading
import queue
from multiprocessing.pool import ThreadPool

import cherrypy

class ResponseBuilder(object):
    """
    Temporary node created to finally service requests. Aware of the matched
    routes upon its instantiation, it parses URL arguments and samples plugin
    methods to construct a response document.
    """
    def __init__(self, nodes):
        self.nodes = nodes

    exposed = True

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, **kwargs):
        return self.get(**kwargs)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self, **kwargs):
        value = cherrypy.request.json
        return self.set(value, **kwargs)

    @staticmethod
    def casted_kwargs(**kwargs):
        if 'sample_rate' in kwargs:
            kwargs['sample_rate'] = min(float(kwargs['sample_rate']), 1000) # TODO parameter
        if 'duration' in kwargs:
            kwargs['duration'] = float(kwargs['duration'])
        if 'leaves_only' in kwargs:
            kwargs['leaves_only'] = bool(kwargs['leaves_only'])
        if 'timeout' in kwargs:
            kwargs['timeout'] = float(kwargs['timeout'])
        return kwargs

    def get(self, **kwargs):
        func = functools.partial(ResponseBuilder.wrapped_plugin_method, '#getter', None)
        kwargs = ResponseBuilder.casted_kwargs(**kwargs)
        return self.handle_parallel(func, **kwargs)

    def set(self, value, **kwargs):
        func = functools.partial(ResponseBuilder.wrapped_plugin_method, '#setter', value)
        kwargs = ResponseBuilder.casted_kwargs(**kwargs)
        return self.handle_parallel(func, **kwargs)

    @staticmethod
    def wrapped_plugin_method(method_label, value, node):
        return_value = None
        exception = None
        try:
            func = node.config.get(method_label, None)
            if func is None:
                raise RuntimeError('Method not supported')
            if value is None:
                return_value = func()
            else:
                return_value = func(value)
        except Exception as ex:
            exception = str(ex)
        return node, return_value, exception

    def handle_parallel(self, sample_method, sample_rate=1, duration=1, leaves_only=False, timeout=None):

        if leaves_only:
            self.nodes = self.leaf_nodes()

        if not self.nodes:
            return {}

        with ThreadPool(len(self.nodes)) as pool:

            result_queue = queue.Queue()

            def put_map(method, routes):
                result_queue.put(pool.map_async(method, routes))

            timers = []
            sample_times = [i / sample_rate for i in range(int(duration * sample_rate))]

            stop_threads = threading.Event() # TODO make threaded plugins aware of this event
            if timeout is not None:
                threading.Timer(timeout, stop_threads.set).start()

            for sample_time in sample_times:
                timer = threading.Timer(sample_time, put_map, [sample_method, self.nodes])
                timers.append(timer)
                timer.start()

            for timer in timers:
                timer.join()

            results = []
            while not result_queue.empty():
                async_result = result_queue.get()
                result = async_result.get()
                results.append(result)

            response = {}
            for routes in results:
                for node, sample, exception in routes:
                    if node.route not in response:
                        response[node.route] = {
                            'units': node.config.get('#units', None),
                            'start-time': cherrypy.response.time,
                            'samples': [],
                            'exceptions': []
                        } #TODO OData compliance here
                    if sample is not None:
                        response[node.route]['samples'].append(sample)
                    if exception is not None:
                        response[node.route]['exceptions'].append(str(exception))
            return response

    def leaf_nodes(self):
        return [x for x in self.nodes if x.config.get('#units',None) != "PathNode"]
