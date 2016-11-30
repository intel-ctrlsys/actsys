# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Implementation of a cluster configuration parser"""
from __future__ import print_function
import re
from ...json_parser.json_parser import JsonParser
from .cluster_configuration_data import ClusterConfigurationData
from ...objects.device import Device


class ListExpander(object):
    """ Expands a list in a string """

    expandable_list_pattern = r',|\[\d:\d+-\d+\]'
    list_pattern = r'(?P<LIST>\[(?P<LENGTH>\d+):(?P<START>\d+)-(?P<END>\d+)\])'
    regex_expandable_list = re.compile(expandable_list_pattern)
    regex_list_pattern = re.compile(list_pattern)

    @classmethod
    def build_item_list(cls, head, length, start, end, tail):
        """Build a list with a defined range, and a head and tail strings"""
        result_list = []
        for digit in range(start, end+1):
            token = "{:s}{:0{:d}d}{:s}".format(head, digit, length, tail)
            result_list.extend(cls.expand_item(token))
        return result_list

    @classmethod
    def expand_item(cls, token):
        """Expand an item returning a list with the expansions"""
        result_list = []
        token_substrings = cls.regex_list_pattern.split(token, 1)
        if len(token_substrings) is 1:
            result_list.append(token_substrings[0])
        else:
            head, _, length, start, end, tail = token_substrings
            result_list.extend(cls.build_item_list(head,
                                                   int(length),
                                                   int(start),
                                                   int(end),
                                                   tail))
        return result_list

    @classmethod
    def is_expandable(cls, string):
        """ Indicates if a string can be expanded or not """
        return cls.regex_expandable_list.search(string)

    @classmethod
    def expand_list(cls, compressed_list):
        """ Receives a string with a list inside and expands that list
            returning a list of the resultant strings"""
        result_list = []
        token_list = compressed_list.replace(' ', '').split(',')
        for token in [x for x in token_list if len(x) > 0]:
            result_list.extend(cls.expand_item(token))
        return result_list


class ClusterConfigurationParser(object):
    """ Cluster Configuration Parser """
    supported_file_versions = ['1', '']
    known_ids = ['device_id', 'hostname', 'ip_address']
    known_types = {
        'NODE_TAG': 'node',
        'BMC_TAG': 'bmc',
        'PDU_TAG': 'pdu',
        'PSU_TAG': 'psu',
        'CONFIG_VARS_TAG': 'configuration_variables'
    }
    __hostname_pattern = r'^([0-9]*[a-zA-Z]|' \
                         r'[0-9]*[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])$'
    __regex_hostname = re.compile(__hostname_pattern)
    __ip_pattern = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)' \
                   r'{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    __regex_ip = re.compile(__ip_pattern)

    def __init__(self, file_path):
        self.file_parser = JsonParser()
        self.data = self.file_parser.read_file(file_path)
        self.parsed_data = ClusterConfigurationData()
        self.profiles = {}

    def parse(self):
        """ Parse function fills the parsed_data object """
        ignored_types = ['profile']

        if self.data.get('version','') not in self.supported_file_versions:
            return False

        types = [device_type for device_type in self.data
                 if device_type not in ignored_types]

        self.__parse_profile__(self.data.get('profile', {}))

        for device_type in types:
            if device_type in self.data:
                self.__parse_type__(device_type, self.data[device_type])

        self.__set_relationships__()
        return True


    def __set_relationships__(self):
        relationship_methods = {
            self.known_types['NODE_TAG']:
                self.__set_node_rel__,
            self.known_types['PDU_TAG']:
                self.__set_power_outlet_rel__,
            self.known_types['PSU_TAG']:
                self.__set_power_outlet_rel__
        }

        for device_type in relationship_methods:
            relationship_methods[device_type](device_type)

    def __set_node_rel__(self, device_type):
        for device_id in self.parsed_data.get(device_type, {}):
            device = self.parsed_data[device_type].get(device_id)
            update_bmc(device, self.parsed_data.search_device(device.bmc, \
                       self.known_types['BMC_TAG']))

    def __set_power_outlet_rel__(self, device_type):
        attribute_name = '{0}_list'.format(device_type)
        for device_id in self.parsed_data.get(device_type, {}):
            device = self.parsed_data[device_type].get(device_id)
            self.__search_rel_per_outlet__(device, attribute_name)

    def __search_rel_per_outlet__(self, device, attribute_name):
        if not device or not device.connected_device:
            return
        for outlet in device.connected_device:
            relationship_info = (device.device_id, outlet.get('outlet'))
            for connected_device in outlet.get('device', []):
                if ListExpander.is_expandable(connected_device):
                    connected_device_list = \
                        ListExpander.expand_list(connected_device)
                else:
                    connected_device_list = [connected_device]
                for device_id in connected_device_list:
                    target_device = self.parsed_data.search_device(device_id)
                    update_power_outlet_list(target_device, relationship_info,
                                             attribute_name)

    def print_parse_data(self):
        """ Prints parsed data object """
        for it1 in self.parsed_data:
            print(it1)
            for it2 in self.parsed_data[it1]:
                print('\t{0}'.format(self.parsed_data[it1][it2]))

    def __parse_profile__(self, object_container):
        parse_method = {list: self.__parse_profile_list__,
                        dict: self.__parse_profile_item__}
        if object_container.__class__ in parse_method:
            parse_method[object_container.__class__](object_container)

    def __parse_profile_list__(self, profile_list):
        for profile in profile_list:
            self.__parse_profile_item__(profile)

    def __parse_profile_item__(self, profile):
        profile_name = profile.pop('profile_name', None)
        if profile_name:
            self.__remove_all_device_id__(profile)
            self.profiles[profile_name] = profile

    def __parse_type__(self, device_type, object_container):
        parse_method = {list: self.__parse_type_list__,
                        dict: self.__parse_item__}
        if object_container.__class__ in parse_method:
            parse_method[object_container.__class__](device_type,
                                                     object_container)

    def __parse_type_list__(self, device_type, type_list):
        for item in type_list:
            self.__parse_item__(device_type, item, True)

    def __parse_item__(self, device_type, item, is_item_list=False):
        self.__replace_profile__(item)
        if device_type in self.known_types.values():
            self.__parse_known_item__(device_type, item)
        else:
            self.__parse_unknown__(device_type, item, is_item_list)

    def __parse_known_item__(self, device_type, item):
        if device_type == self.known_types['CONFIG_VARS_TAG']:
            item['device_id'] = device_type
        device_id = self.__find_id__(item)
        if device_id:
            self.__store_item__(device_type, device_id, item)

    def __remove_all_device_id__(self, profile):
        for id_attribute in self.known_ids:
            profile.pop(id_attribute, None)

    def __find_id__(self, item):
        for id_attribute in self.known_ids:
            if id_attribute in item:
                return item[id_attribute]
        return None

    def __replace_profile__(self, item):
        profile = self.profiles.get(item.pop('profile', None))
        if profile:
            profile = profile.copy()
            profile.update(item)
            item.update(profile)

    def __store_group_item__(self, group):
        item_list = expand_group(group)
        for item in item_list:
            self.__add_device__(item)

    def __store_item__(self, device_type, device_id, item):
        item['device_type'] = device_type
        item['device_id'] = device_id
        if ListExpander.is_expandable(device_id):
            self.__store_group_item__(item)
        else:
            self.__add_device__(item)

    def __add_device__(self, item):
        if item.get('hostname') and \
            not self.__is_valid_hostname__(item.get('hostname')):
            return
        if item.get('ip_address') and \
            not self.__is_valid_ip_addr__(item.get('ip_address')):
            return
        self.parsed_data.add_device(Device(item))

    def __is_valid_hostname__(self, hostname):
        return self.__regex_hostname.match(hostname) is not None

    def __is_valid_ip_addr__(self, ip_addr):
        return self.__regex_ip.match(ip_addr) is not None

    def __parse_unknown__(self, device_type, item, is_item_list):
        device_id = self.__find_id__(item)
        if is_item_list and not device_id:
            return
        if device_id:
            self.__store_item__(device_type, device_id, item)
        else:
            self.__store_item__(device_type, device_type, item)


def update_bmc(device, bmc):
    """ Updates  bmc attribute in a device object """
    if device:
        device.__update_dict__(dict(bmc=bmc))


def update_power_outlet_list(device, info, attribute_name):
    """ Updates the list in attribute name with the given info """
    if not device or not info or not attribute_name:
        return
    if device.__dict__.get(attribute_name):
        device.__dict__[attribute_name].append(info)
    else:
        device.__update_dict__({attribute_name: [info]})


def get_min_length(lists):
    """ List of lists,
    returns the length of the shorter list. """
    if not lists:
        return 0
    min_length = len(lists[0])
    for list_ in lists:
        if len(list_) < min_length:
            min_length = len(list_)
    return min_length


def fix_lists_length(lists_dict):
    """ @param lists_dict - Dictionary of lists
    This function will fix the length of all the lists inside
    the given dictionary to the length of the shorter list.
    """
    if not lists_dict:
        return
    min_length = get_min_length(lists_dict.values())
    for attribute in lists_dict:
        lists_dict[attribute] = \
            lists_dict[attribute][:min_length]


def create_group_items(base_item, expanded_attributes):
    """ This function will create a list of items
    based on the given base_item and append or update
    the attributes given in expanded_attributes dictionary
    for each of the items that will be created.
    """
    result_list = []
    if not expanded_attributes.get('device_id'):
        return result_list
    for index in xrange(len(expanded_attributes.get('device_id'))):
        item = base_item.copy()
        for attribute in expanded_attributes:
            item[attribute] = expanded_attributes[attribute][index]
        result_list.append(item)
    return result_list


def expand_attributes(group, attributes_list):
    """ For each attribute in group (included in attributes_list),
    this function will expand its content in case it represents a list. """
    expanded_attributes = {}
    if attributes_list:
        for attribute in attributes_list:
            if group.get(attribute):
                expanded_attributes[attribute] = \
                    ListExpander.expand_list(group[attribute])
    return expanded_attributes


def expand_group(group):
    """" Expands attributes for group and create a list of items
    with those attributes """
    if not group:
        return []
    expanded_attributes = expand_attributes(group, \
        ['device_id', 'bmc', 'hostname', 'ip_address'])
    fix_lists_length(expanded_attributes)
    return create_group_items(group, expanded_attributes)
