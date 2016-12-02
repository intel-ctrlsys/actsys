# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Module that defines a read only object with dynamic number of attributes"""


class ConfigurationManagerItem(object):
    """ Base class of a Configuration  Manager Object"""

    def __init__(self, attributes=None):
        """ Init function, you can only add a dictionary of attributes
         at this step.
        :type attributes: dict
        """
        if attributes is not None:
            self.__update_dict__(attributes)

    def __update_dict__(self, new_attributes):
        """ Function to update internal dictionary
        :type new_attributes: dict
        :param new_attributes: dictionary to add attributes or update values
        """
        self.__dict__.update(new_attributes)

    def __add_attribute__(self, name, value):
        """Allows to add an attribute to an existent object"""
        new_attribute = dict({name: value})
        self.__update_dict__(new_attribute)

    def get_attribute_list(self):
        """Allow access to the list of attributes of this object"""
        return vars(self).keys()

    def __repr__(self):
        """ Transfer the object's representation to the one of __dict__"""
        return self.__dict__.__repr__()

    def __getattr__(self, item):
        """ Getattr function, if we try to access to a non existent attribute
        then we must return None
        """
        return None

    def __setattr__(self, key, value):
        """ Overrides setattr function so attributes can be read-only """
        pass

    def __reduce_ex__(self, _):
        return (self.__class__, (self.__dict__, ))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ <> other.__dict__
        return True
