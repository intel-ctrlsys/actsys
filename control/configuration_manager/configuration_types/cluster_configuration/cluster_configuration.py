# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Implementation of a configuration object and his extractor"""
from . cluster_configuration_extractor_interface \
    import ClusterConfigurationExtractorInterface

from .cluster_configuration_data import ClusterConfigurationData
from ..configuration_type_interface import ConfigurationTypeInterface
from ...json_parser.json_parser import JsonParser


class ClusterConfigurationExtractor(ClusterConfigurationExtractorInterface):
    """Implements ClusterConfigurationExtractorInterface interface"""
    NODE_TAG = 'node'
    BMC_TAG = 'bmc'
    PSU_TAG = 'psu'
    PDU_TAG = 'pdu'
    CONFIG_VARS_TAG = 'configuration_variables'

    def __init__(self, data_container):
        """init method
        :param data_container: Object storing the data
        """
        self.data_container = data_container

    def get_device(self, device_id):
        """Implements get_device
        :rtype: Device
        :param device_id: Unique id of a device
        :return: A Device Object
        """
        return self.data_container.search_device(device_id)

    def get_devices_by_type(self, device_type):
        """Implements get_devices_by_type
        :rtype: Device
        :param device_type: Unique id of a device type
        :return: A Device Object dictionary
                 None, in case device_type doesn't exist
        """
        return self.data_container.get(device_type)


    def get_node(self, device_id):
        """Implements get_node
        :rtype: Device
        :param device_id: Unique id of a node
        :return: A Device Object"""
        return self.data_container.search_device(device_id, self.NODE_TAG)

    def get_bmc(self, device_id):
        """Implements get_bmc
        :rtype: Device
        :param device_id: Unique id of a bmc
        :return: A Device Object"""
        return self.data_container.search_device(device_id, self.BMC_TAG)

    def get_psu(self, device_id):
        """Implements get_psu
        :rtype: Device
        :param device_id: Unique id of a psu
        :return: A Device Object"""
        return self.data_container.search_device(device_id, self.PSU_TAG)

    def get_pdu(self, device_id):
        """Implements get_pdu
        :rtype: Device
        :param device_id: Unique id of a pdu
        :return: A Device Object"""
        return self.data_container.search_device(device_id, self.PDU_TAG)

    def get_config_vars(self):
        """Implements get_config_vars
        :rtype: Device
        :return: A Device Object with the Global Configuration Variables"""
        return self.data_container.search_device(self.CONFIG_VARS_TAG,
                                                 self.CONFIG_VARS_TAG,)


class ClusterConfiguration(ConfigurationTypeInterface):
    """Implements ConfigurationTypeInterface interface"""

    def __init__(self, file_path):
        """ init method
        :param file_path: path to the config file
        """
        super(ClusterConfiguration, self).__init__(file_path)

    def get_extractor(self):
        """Implements get_extractor
        :rtype: ClusterConfigurationExtractorInterface
        :return: An extractor Object
        """
        return self.extractor

    def parse(self):
        """Implements parse
        :rtype: bool
        :return: True if this object can parse or False if not
        """
        self.parser = JsonParser()
        self.data = ClusterConfigurationData(True)
        self.extractor = ClusterConfigurationExtractor(self.data)
        return True
