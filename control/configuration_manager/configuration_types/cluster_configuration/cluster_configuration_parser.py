# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Implementation of a cluster configuration parser"""
from __future__ import print_function
from ...json_parser.json_parser import JsonParser
from .cluster_configuration_data import ClusterConfigurationData
from ...objects.device import Device

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
        device.__update_dict__({attribute_name:[info]})


class ClusterConfigurationParser(object):
    """ Cluster Configuration Parser """
    known_ids = ['device_id', 'hostname', 'ip_address']
    known_types = {
        'NODE_TAG':'node',
        'BMC_TAG':'bmc',
        'PDU_TAG':'pdu',
        'PSU_TAG':'psu',
        'CONFIG_VARS_TAG':'configuration_variables'
    }
    def __init__(self, file_path):
        self.file_parser = JsonParser()
        self.data = self.file_parser.read_file(file_path)
        self.parsed_data = ClusterConfigurationData()
        self.profiles = {}

    def parse(self):
        """ Parse function fills the parsed_data object """
        ignored_types = ['profile']
        if not self.data:
            return
        types = [device_type for device_type in self.data
                 if device_type not in ignored_types]

        self.__parse_profile__(self.data.get('profile', {}))

        for device_type in types:
            if device_type in self.data:
                self.__parse_type__(device_type, self.data[device_type])

        self.__set_relationships__()


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
                target_device = self.parsed_data.search_device(connected_device)
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
        self.__replace_profile(item)
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

    def __is_expandable(self, item):
        # todo implement this
        return False

    def __remove_all_device_id__(self, profile):
        for id_attribute in self.known_ids:
            profile.pop(id_attribute, None)

    def __find_id__(self, item):
        for id_attribute in self.known_ids:
            if id_attribute in item:
                return item[id_attribute]
        return None

    def __replace_profile(self, item):
        profile = self.profiles.get(item.pop('profile', None))
        if profile:
            profile = profile.copy()
            profile.update(item)
            item.update(profile)

    def __store_group_item__(self, group):
        item_list = self.expand_group(group)
        for item in item_list:
            self.__store_item__(item['device_type'], item['device_id'], item)

    def expand_group(self, group):
        # todo make this actually work
        return [group]

    def __store_item__(self, device_type, device_id, item):
        item['device_type'] = device_type
        item['device_id'] = device_id
        if self.__is_expandable(item):
            self.__store_group_item__(item)
        else:
            self.parsed_data.add_device(Device(item))

    def __parse_unknown__(self, device_type, item, is_item_list):
        device_id = self.__find_id__(item)
        if is_item_list and not device_id:
            return
        if device_id:
            self.__store_item__(device_type, device_id, item)
        else:
            self.__store_item__(device_type, device_type, item)
