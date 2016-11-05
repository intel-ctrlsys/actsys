# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Module that defines base clase for cluster representation objects """


class Device(object):
    """ Base class to represent a device in a cluster configuration """

    def __init__(self, attributes=None):
        """ Init function """
        if attributes is not None:
            self.__update_dict__(attributes)

    def __update_dict__(self, new_attributes):
        """ Function to update internal dictionary """
        self.__dict__.update(new_attributes)

    def __add_attribute__(self, attribute_name, attribute_value):
        """Allows to add an attribute"""
        new_attribute = dict({attribute_name: attribute_value})
        self.__update_dict__(new_attribute)

    def get_attribute_list(self):
        """Allow access to the list of attributes of this object"""
        return vars(self).keys()

    def __repr__(self):
        """ Transfer the object's representation to the one of __dict__"""
        return self.__dict__.__repr__()

    def __getattr__(self, item):
        """ Getattr function """
        return None

    def __setattr__(self, key, value):
        """ Overrides setattr function so attributes can be read-only """
        pass
