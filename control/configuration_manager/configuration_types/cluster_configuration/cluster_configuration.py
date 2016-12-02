# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Implementation of a configuration object and his extractor"""
import copy
from . cluster_configuration_extractor_interface \
    import ClusterConfigurationExtractorInterface
from .cluster_configuration_parser \
    import ClusterConfigurationParser as CCParser
from ..configuration_type_interface import ConfigurationTypeInterface
from .cluster_configuration_data \
    import ClusterConfigurationData

class ClusterConfigurationExtractor(ClusterConfigurationExtractorInterface):
    """Implements ClusterConfigurationExtractorInterface interface"""
    NODE_TAG = CCParser.known_types['NODE_TAG']
    BMC_TAG = CCParser.known_types['BMC_TAG']
    PSU_TAG = CCParser.known_types['PSU_TAG']
    PDU_TAG = CCParser.known_types['PDU_TAG']
    CONFIG_VARS_TAG = CCParser.known_types['CONFIG_VARS_TAG']

    def __init__(self, data):
        """init method
        :param data: Object storing the data
        """
        if not isinstance(data, ClusterConfigurationData):
            raise TypeError()
        self.data = data

    def get_device(self, device_id):
        """Implements get_device
        :rtype: Device
        :param device_id: Unique id of a device
        :return: A Device Object
        """
        return copy.deepcopy(self.data.search_device(device_id))

    def get_device_types(self):
        return self.data.keys()

    def get_devices_by_type(self, device_type):
        """Implements get_devices_by_type
        :rtype: Device
        :param device_type: Unique id of a device type
        :return: A Device Object dictionary
                 None, in case device_type doesn't exist
        """
        return copy.deepcopy(self.data.get(device_type, {}))


    def get_node(self, device_id):
        """Implements get_node
        :rtype: Device
        :param device_id: Unique id of a node
        :return: A Device Object"""
        return copy.deepcopy(self.data.search_device(device_id, self.NODE_TAG))

    def get_bmc(self, device_id):
        """Implements get_bmc
        :rtype: Device
        :param device_id: Unique id of a bmc
        :return: A Device Object"""
        return copy.deepcopy(self.data.search_device(device_id, self.BMC_TAG))

    def get_psu(self, device_id):
        """Implements get_psu
        :rtype: Device
        :param device_id: Unique id of a psu
        :return: A Device Object"""
        return copy.deepcopy(self.data.search_device(device_id, self.PSU_TAG))

    def get_pdu(self, device_id):
        """Implements get_pdu
        :rtype: Device
        :param device_id: Unique id of a pdu
        :return: A Device Object"""
        return copy.deepcopy(self.data.search_device(device_id, self.PDU_TAG))

    def get_config_vars(self):
        """Implements get_config_vars
        :rtype: Device
        :return: A Device Object with the Global Configuration Variables"""
        return copy.deepcopy(self.data.search_device(self.CONFIG_VARS_TAG,
                                                     self.CONFIG_VARS_TAG))


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
        self.parser = CCParser(self.file_path)
        if self.parser.parse():
            self.data = self.parser.parsed_data
            self.extractor = ClusterConfigurationExtractor(self.data)
            return True
        return False
