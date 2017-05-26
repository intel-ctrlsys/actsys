# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 <company or person>
#
"""
The entry point for this application.
"""
from __future__ import print_function

__version__ = "0.1.0"


class StartExample(object):
    """
    A example class that is the starts this application
    """

    def __init__(self):
        """
        Starter Example constructor. Used to setup before running.
        """
        self.location = "World"

    def run(self):
        """
        Run your application.
        :return:
        """
        self.print_version()
        print("Hello {}!".format(self.location))

    def print_version(self):
        """
        Print the version
        :return:
        """
        print("Version: {}".format(__version__))
