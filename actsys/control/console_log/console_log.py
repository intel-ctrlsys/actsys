# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""Interface for all console_log plugin"""
from control.plugin import DeclareFramework


@DeclareFramework('console_log')
class ConsoleLog(object):
    """interface for console log classes"""
    def __init__(self, **options):
        pass

    def start_log_capture(self, stop_line, result_line):
        """Start capturing console"""
        pass

    def stop_log_capture(self):
        """Stop capture"""
        pass
