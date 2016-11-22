# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Module that defines base clase for cluster representation objects """
from .configuration_manager_item import ConfigurationManagerItem


class Device(ConfigurationManagerItem):
    """ Base class to represent a device in a cluster configuration """

    def __init__(self, attributes=None):
        """ Init function
        :type attributes: dict
        """
        if not attributes:
            attributes = dict({})

        if 'device_id' not in attributes:
            attributes['device_id'] = None

        if 'device_type' not in attributes:
            attributes['device_type'] = None
        super(Device, self).__init__(attributes)
