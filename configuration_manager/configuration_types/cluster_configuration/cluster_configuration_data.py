# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
""" Utility class for Configuration Manager"""
from ctrl.configuration_manager.objects.device import Device
from ctrl.utilities.remote_access_data import RemoteAccessData


def __is_a_valid_device__(device):
    if device is None or \
            not isinstance(device, Device) or \
                    device.device_type is None or \
                    device.device_id is None:
        return False
    return True


class ClusterConfigurationData(dict):
    """ Class that will hold the logic from the configuration file """

    def __init__(self, test=False):
        """ Init function """
        super(ClusterConfigurationData, self).__init__()
        if test:
            self.__fill_dummy_data__()

    def __fill_dummy_data__(self):
        service = Device(dict(orcmd=dict(service_type="Sensys",
                                         serivce_attributes={'verbose': 100})))
        rad1 = RemoteAccessData("192.168.1.100", 8080, "root", "rootpaswd")
        node_dict = dict(device_type='NODE', device_id="host1", rad=rad1, \
                         node_type="aggregator", \
                         image="/images/myimage.ino", \
                         services=service, bmc_id="bmc1", \
                         pdus=["pdu1", "pdu2"], psus=["psu1"])
        node1 = Device(node_dict)
        print self.add_device(node1)

    def add_device(self, device):
        """ This function allows to add a device """
        try:
            self[device.device_type] = device
            return True
        except:
            return False

    def __setitem__(self, key, device):
        if not __is_a_valid_device__(device):
            raise TypeError
        print "set item", key
        if key in self.keys():
            self[key][device.device_id] = device
        else:
            super(ClusterConfigurationData, self).__setitem__(key,
                                                {device.device_id: device})

    def search_device(self, device_id, device_type=None):
        """ Searches a device by its device_id and device_type (optionally) """
        if device_type is None:
            for dtype in self.keys():
                if device_id in self[dtype].keys():
                    return self[dtype][device_id]
        elif device_type in self.keys():
            return self[device_type].get(device_id)
        return None
