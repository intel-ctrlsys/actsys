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
    start_time = time.time()
    wrapped_method = wrap_method(method_label, method_args, method_kwargs)
    results = parallel_apply_method(wrapped_method, nodes, **request_kwargs)
    return document_from_results(results, start_time)


def document_from_results(results, start_time):
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


def wrap_method(method_label, args, kwargs):
    def wrapped_plugin_method(node):
        try:
            return node, node.get_method(method_label)(*args, **kwargs), None
        except Exception as ex:
            return node, None, str(ex)
    return wrapped_plugin_method


def parallel_apply_method(method, nodes, sample_rate=1, duration=1, leaves_only=False):
    """
    Apply method to every node in nodes, sample_rate times per second, for duration seconds.
    Returns a list of results for each time slice. Each time slice result is a list of tuples
    (node, return value, string-casted exception) showing that time slice's results.
    """
    if leaves_only:
        nodes = [x for x in nodes if x.config.get('#units', None) != "PathNode"]
    if not nodes:
        return {}
    with ThreadPool(len(nodes)) as pool:
        time_slice_results = queue.Queue()
        def apply_time_slice():
            time_slice_results.put(pool.map_async(method, nodes))
        num_slices = int(duration * sample_rate)
        slice_times = [slice_number / sample_rate for slice_number in range(num_slices)]
        time_slice_threads = [threading.Timer(time, apply_time_slice) for time in slice_times]
        complete_all_threads(time_slice_threads)
        return consume_queue(time_slice_results)

def complete_all_threads(threads):
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def consume_queue(result_queue):
    results = []
    while not result_queue.empty():
        results.append(result_queue.get().get())
    return results
