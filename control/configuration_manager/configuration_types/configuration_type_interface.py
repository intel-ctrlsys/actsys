# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Abstract class"""
from abc import ABCMeta, abstractmethod


class ConfigurationTypeInterface(object):
    """Abstract class for a configuration object"""
    __metaclass__ = ABCMeta

    def __init__(self, file_path):
        """init of the class"""
        self.file_path = file_path
        self.extractor = None
        self.data = None
        self.parser = None

    @abstractmethod
    def parse(self):
        """This method evaluate if the given file can be interpreted"""
        raise NotImplementedError()

    @abstractmethod
    def get_extractor(self):
        """This method return the extractor of this configuration object"""
        raise NotImplementedError()
