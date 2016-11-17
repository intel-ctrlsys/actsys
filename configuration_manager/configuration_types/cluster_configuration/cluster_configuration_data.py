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

def __create_dummy_bmc__():
    rad = RemoteAccessData('192.168.2.32', 20, 'username', 'pass@123')
    return Device(dict(device_type='bmc', device_id=rad.address, \
                      rad=rad, channel=11, priv_level='USER', \
                      auth_method='PASSWORD'))

def __create_dummy_node__(bmc):
    rad = RemoteAccessData('192.168.1.32', 20, 'username', 'pass@123')
    return Device(dict(device_type='node', device_id='master4', rad=rad, \
                       role=['aggregator'], image='/images/myimage.ino', \
                       service_list=['gmond', 'orcmd', 'orcmsched'], \
                       bmc=bmc, \
                       os_shutdown_timeout_seconds=150,\
                       os_boot_timeout_seconds=300, \
                       os_network_to_halt_time=5, \
                       bmc_boot_timeout_seconds=10, \
                       bmc_chassis_off_wait=3, \
                       pdu_list=[('192.168.3.32', 3)], \
                       psu_list=[('192.168.4.32', 1)]))

def __create_dummy_pdu__():
    rad = RemoteAccessData('192.168.3.32', 20, 'username', 'pass@123')
    return Device(dict(device_type='pdu', device_id=rad.address, rad=rad, \
                      outlets_count=12, \
                      connected_device=[{'outlet':'3', \
                      'device':'master4'}, {'outlet':'0', \
                      'device':'192.168.4.32'}]))

def __create_dummy_psu__():
    rad = RemoteAccessData('192.168.4.32', 20, 'username', 'pass@123')
    return Device(dict(device_type='psu', device_id=rad.address, rad=rad, \
                      outlets_count=2, \
                      connected_device=[{'outlet':'1', 'device':'master4'},\
                      {'outlet':'0', 'device':'master3'}]))

def __create_dummy_config_vars__():
    return Device(dict(device_type='configuration_variables', \
                         device_id='configuration_variables', \
                         provisioning_agent_software='Warewulf', \
                         log_file={'path':'/var/log/ctrl.log', \
                         'max_bytes':10485760, 'level':'DEBUG', \
                         'retention_period':30},\
                         console_output={'file':['/opt/ctrl/console'], \
                         'error_level_regex':['regex'], \
                         'warning_level_regex':['regex']}))


class ClusterConfigurationData(dict):
    """ Class that will hold the logic from the configuration file """

    def __init__(self, test=False):
        """ Init function """
        super(ClusterConfigurationData, self).__init__()
        if test:
            self.__fill_dummy_data__()

    def __fill_dummy_data__(self):
        bmc = __create_dummy_bmc__()
        self.add_device(bmc)
        self.add_device(__create_dummy_node__(bmc))
        self.add_device(__create_dummy_pdu__())
        self.add_device(__create_dummy_psu__())
        self.add_device(__create_dummy_config_vars__())


    def add_device(self, device):
        """ This function allows to add a device """
        try:
            self[device.device_type] = device
            return True
        except (TypeError, AttributeError):
            return False

    def __setitem__(self, key, device):
        if not __is_a_valid_device__(device):
            raise TypeError
        if key in self.keys():
            self[key][device.device_id] = device
        else:
            super(ClusterConfigurationData, self).__setitem__(key,\
                  {device.device_id: device})

    def search_device(self, device_id, device_type=None):
        """ Searches a device by its device_id and device_type (optionally) """
        if not device_type:
            for dtype in self.keys():
                if device_id in self[dtype].keys():
                    return self[dtype][device_id]
        elif device_type in self.keys():
            return self[device_type].get(device_id)
        return None
