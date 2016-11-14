# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Abstract class"""
from abc import ABCMeta, abstractmethod


class ClusterConfigurationExtractorInterface(object):
    """Abstract class defining methods to query data"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_device(self, device_id):
        """Returns a device object matching with the given id"""
        raise NotImplementedError()

    @abstractmethod
    def get_devices_by_type(self, device_type):
        """Returns a device object matching with the given id"""
        raise NotImplementedError()

    @abstractmethod
    def get_bmc(self, bmc_id):
        """Returns a device object matching with the given id.
            This method will search only for bmc objects
        """
        raise NotImplementedError()

    @abstractmethod
    def get_node(self, node_id):
        """Returns a device object matching with the given id.
            This method will search only for node objects
        """
        raise NotImplementedError()

    @abstractmethod
    def get_psu(self, psu_id):
        """Returns a device object matching with the given id.
            This method will search only for psu objects
        """
        raise NotImplementedError()

    @abstractmethod
    def get_pdu(self, pdu_id):
        """Returns a device object matching with the given id.
            This method will search only for pdu objects
        """
        raise NotImplementedError()

    @abstractmethod
    def get_rack(self, rack_id):
        """Returns a device object matching with the given id.
            This method will search only for rack objects
        """
        raise NotImplementedError()
