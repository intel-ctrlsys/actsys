# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Configuration Manager main module"""

from ctrl.configuration_manager.configuration_types.cluster_configuration. \
    cluster_configuration import ClusterConfiguration


class ConfigurationManager(object):
    """ Configuration Manager main class"""
    __file_types = {'ClusterConfiguration': [ClusterConfiguration]}
    __configuration_objects = {}

    def __new__(cls, file_path, file_type='ClusterConfiguration'):
        """ Override to make this class a Singleton"""
        if not hasattr(cls, 'unique_instance'):
            cls.unique_instance = super(ConfigurationManager, cls).__new__(
                cls, file_path, file_type)

        return cls.unique_instance

    def __init__(self, file_path, file_type='ClusterConfiguration'):
        """ Init method selects a configuration object if there is no one
            for the type given.
        """
        if file_type not in self.__configuration_objects.keys():
            configuration_object = \
                self.__get_configuration_object(file_path, file_type)
            if configuration_object is not None:
                self.__configuration_objects[file_type] = configuration_object

    def __get_configuration_object(self, file_path,
                                   file_type='ClusterConfiguration'):
        """ Returns a configuration object capable to read the given file"""
        objects = self.__file_types[file_type]
        for candidate in objects:
            configuration_object = candidate(file_path)
            if configuration_object.parse():
                return configuration_object

    def get_extractor(self, file_type='ClusterConfiguration'):
        """ Returns a extractor to query data"""
        extractor = None
        if file_type in self.__configuration_objects.keys():
            extractor = self.__configuration_objects[file_type].get_extractor()
        return extractor
