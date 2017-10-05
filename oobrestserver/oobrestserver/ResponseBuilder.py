# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Exposes the generate_document function, which builds responses for the server.
"""

import threading
import time
import queue
from multiprocessing.pool import ThreadPool


def generate_document(nodes, method_label, method_args, method_kwargs, request_kwargs):
    func = wrap_method(method_label, method_args, method_kwargs)
    return handle_parallel(nodes, func, **request_kwargs)


def wrap_method(method_label, args, kwargs):
    def wrapped_plugin_method(node):
        try:
            return node, node.get_method(method_label)(*args, **kwargs), None
        except Exception as ex:
            return node, None, str(ex)
    return wrapped_plugin_method


def handle_parallel(nodes, sample_method, sample_rate=1, duration=1, leaves_only=False, timeout=None):

    if leaves_only:
        nodes = [x for x in nodes if x.config.get('#units', None) != "PathNode"]

    if not nodes:
        return {}

    with ThreadPool(len(nodes)) as pool:

        result_queue = queue.Queue()

        def enqueue_map_results(method, routes):
            result_queue.put(pool.map_async(method, routes))

        start_time = time.time()
        timers = []
        sample_times = [i / sample_rate for i in range(int(duration * sample_rate))]

        stop_threads = threading.Event()
        if timeout is not None:
            threading.Timer(timeout, stop_threads.set).start()

        for sample_time in sample_times:
            timer = threading.Timer(sample_time, enqueue_map_results, [sample_method, nodes])
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
                        'start-time': start_time,
                        'samples': [],
                        'exceptions': []
                    }
                if sample is not None:
                    response[node.route]['samples'].append(sample)
                if exception is not None:
                    response[node.route]['exceptions'].append(str(exception))
        return response
