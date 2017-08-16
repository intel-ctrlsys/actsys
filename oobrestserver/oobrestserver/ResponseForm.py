# -*- coding: utf-8 -*-
"""Defines the ResponseForm class for use by the server for each request."""

import time


class ResponseForm(object):
    """Describes the under-construction response to an in-flight request."""

    def __init__(self):
        self.data = {
            'units': None,
            'start-time': time.time(),
            'samples': [],
            'exceptions': []
        }

    def add_sample_from_func(self, func, *args):
        try:
            self.add_sample(func(*args))
        except Exception as ex:
            self.data['exceptions'].append(str(ex))

    def add_samples_over_time(self, sample_rate_arg, duration_arg, func, *args):
        """Add samples from func to response at sample_rate for duration."""
        sample_rate = float(sample_rate_arg)
        duration = float(duration_arg)
        iter_start_time = time.time()
        sample_interval = 1.0 / sample_rate
        end_time = iter_start_time + duration - sample_interval / 2.0
        while iter_start_time < end_time:
            self.add_sample_from_func(func, *args)
            sleep_time = iter_start_time + sample_interval - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            iter_start_time = time.time()

    def add_sample(self, sample):
        self.data['samples'].append(sample)

    def finished_dict(self):
        self.data['end-time'] = time.time()
        return self.data
