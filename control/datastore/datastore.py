# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
from __future__ import print_function
import logging
from abc import ABCMeta, abstractmethod
from .utilities import DataStoreUtilities


class DataStore(object):
    """
    Data Store interface.
    """
    __metaclass__ = ABCMeta
    LOG_LEVEL = logging.DEBUG
    LOG_LEVEL_JOURNAL = 35
    JOURNAL = 35
    SKU = 37

    def __init__(self, print_to_screen):
        self.print_to_screen = print_to_screen
        logging.addLevelName(self.LOG_LEVEL_JOURNAL, "JOURNAL")
        logging.addLevelName(self.SKU, "SKU")
        self.logger = logging.getLogger('DataStore')
        self.logger.setLevel(self.LOG_LEVEL)

    def get_device(self, device_name):
        """
        Here for posterity's sake. Returns the first device found or None.
        :param device_name:
        :return:
        """
        device = self.device_get(device_name)
        if len(device) == 1:
            return device[0]
        else:
            return None

    @abstractmethod
    def device_get(self, device_name=None):
        """
        Get the configuration information of the specified device.

        This includes retrieving and filling out any information that the device
        profile may specify.

        :parameter @device_name is used to locate the device. This happens by first
         searching device_id for a match, then hostname, then ip. So as long
         as these three fields are unique you can ask for a node based on any of
         these fields. DataStore does not enforce uniqueness of names (but underlying implementation may).
         If conflicts ocour, the first found is returned.
        :return: A List of devices
        """
        self._print_if_ok("device_get: {}".format(device_name))
        return list()

    @abstractmethod
    def device_upsert(self, device_info):
        """
        Either updates or creates a device. This device is saved to the DataStore. An update is attempted when device_id
         is passed in via the device_info param. Otherwise, the device is created.
        :param device_info: An object or dict of values that define the device. The only required value is that of device_type.
        :return: the affected device_id
        :raise DataStoreException when device_type is not set in the device_info param
        """
        self._print_if_ok("device_upsert: {}".format(device_info))

        if device_info.get("device_type") is None:
            raise DataStoreException("device_type is a required key/value in the device_info field")

    @abstractmethod
    def device_logical_delete(self, device_name):
        """
        Logically removes a device from the system database. This device will remain in the database, but no longer
        be reachable via getters and setters
        :param device_name: As explained in DataStore.device_get()
        :return: device_id of the affected device or None
        """
        self._print_if_ok("device_logical_delete: {}".format(device_name))

    @abstractmethod
    def device_fatal_delete(self, device_name):
        """
        Remove the device, all logs, and SKUS associated with the device. Be very careful.
        :param device_name: As explained in DataStore.device_get()
        :return: device_id of the affected device or None
        """
        self._print_if_ok("device_fatal_delete: {}".format(device_name))

    @abstractmethod
    def sku_get(self, device_name=None):
        """
        Get SKUs. Filtered by device_name if specified.
        :param device_name: As explained in DataStore.device_get()
        :return: A list of SKUs.
        """
        self._print_if_ok("sku_get: {}".format(device_name))

    @abstractmethod
    def sku_history(self, device_name=None):
        """
        Get the History of SKU changes. Filtered by device_name if specified.
        :param device_name:
        :return: A List of SKUs with attached history metadata.
        """
        self._print_if_ok("sku_history: {}".format(device_name))

    @abstractmethod
    def sku_upsert(self, device_name, sku_name, step=None, hardware_type=None, model_number=None):
        """
        Ether updates or creates a SKU. The SKU is saved to the DataStore. An update is attempted when an existing
        (device_name, sku_name) combo already exists. Otherwise the SKU is created. All changes to SKUs are logged in
        history.
        :param device_name: As explained in DataStore.device_get()
        :param sku_name: id
        :param step:
        :param hardware_type:
        :param model_number:
        :return: The affected SKU id (which is the SKU.sku itself)
        :raise DataStoreException if the device_name does not exist.
        """
        self._print_if_ok("sku_history: {} - {}".format(device_name, sku_name))

    @abstractmethod
    def sku_delete(self, device_name, sku_name):
        """
        Delete a SKU in a given device
        :param device_name: As explained in DataStore.device_get()
        :param sku_name:
        :return: The affected SKU id or None if nothing was done.
        """
        self._print_if_ok("sku_delete: {} - {}".format(device_name, sku_name))

    @abstractmethod
    def profile_get(self, profile_name=None):
        """
        Get profiles. Filtered by profile name, if specified.
        :param profile_name: unique id and reference name of this profile
        :return: A List of profiles
        """
        self._print_if_ok("profile_get: {}".format(profile_name))
        return list()

    @abstractmethod
    def profile_upsert(self, profile_info):
        """
        Either updates or creates a profile. This is saved to the DataStore. An update occurs when the profile_info
        param has a profile_name that already exists.
        :param profile_info: An object or dict of properties to be contained in this profile. profile_name must be
            included in this object/dict
        :return: profile_name
        :raise DataStoreException if profile_name is not set in profile info.
        """
        self._print_if_ok("profile_upsert: {}".format(profile_info))
        if profile_info.get("profile_name") is None:
            raise DataStoreException("Cannot upsert, profile_name must be specified")
        return profile_info.get("profile_name")

    @abstractmethod
    def profile_delete(self, profile_name):
        """
        Attempts to remove a profile. This cannot be done if the profile is in use
        by any other devices.
        :param profile_name: As explained in profile_get()
        :return: profile_name
        :raise DataStoreException if the profile cannot be delete because it is in use by devices.
        """
        self._print_if_ok("profile_delete: {}".format(profile_name))
        return profile_name

    @abstractmethod
    def log_get(self, device_name=None, limit=100):
        """
        If no device_name is specified, returns general logs.
        If device_name is specified, returns device logs.

        :param device_name: As explained in DataStore.device_get()
        :param limit: how many logs are returned?
        :return: A list of Logs
        """
        self._print_if_ok("log_get: {}".format(device_name))

    @abstractmethod
    def log_get_timeslice(self, begin, end, device_name=None, limit=100):
        """

        :param begin: datetime
        :param end: datetime
        :param device_name: As explained in DataStore.device_get()
        :param limit: how many logs to return
        :return: A list of logs
        """
        self._print_if_ok("log_get_timeslice: {} - {}-{}".format(device_name, begin, end))

    @abstractmethod
    def log_add(self, level, msg, device_name=None, process=None):
        """
        Add a log to the datastore.
        :param level: Per spec https://docs.python.org/2/library/logging.html#logging-levels
            with the additional log level of JOURNAL
        :param process:
        :param msg:
        :param device_name: As explained in DataStore.device_get()
        :return: None
        """
        self._print_if_ok("log_add: [{}][{}] {} - {}".format(level, process, device_name, msg))

    @abstractmethod
    def configuration_get(self, key):
        """
        Get the value for a particular key in the configuration
        :param key: str
        :return: value: str or None if the key is not found
        """
        self._print_if_ok("configuration_get: {}".format(key))

    @abstractmethod
    def configuration_upsert(self, key, value):
        """
        Insert the new configuration value, update on key conflict
        :param key: str
        :param value: str
        :return: key
        """
        self._print_if_ok("configuration_upsert: {} / {}".format(key, value))

    @abstractmethod
    def configuration_delete(self, key):
        """
        Delete the value of a given key
        :param key: str
        :return: value: str or None if nothing was deleted.
        """
        self._print_if_ok("configuration_delete: {}".format(key))

    # UTIL FUNCTIONS
    def get_device_types(self):
        devices = self.device_get()
        types = list()
        if devices is None:
            return types

        for device in devices:
            device_type = device.get("device_type")
            if device_type is not None and device_type not in types:
                types.append(device_type)

        return types

    def get_log_levels(self):
        return [
            logging.CRITICAL,
            logging.ERROR,
            self.SKU,
            self.LOG_LEVEL_JOURNAL,
            logging.WARN,
            logging.INFO,
            logging.DEBUG,
            logging.NOTSET
        ]

    def _print_if_ok(self, msg):
        if self.print_to_screen:
            print(msg)

    def get_logger(self):
        """
        The same as running DataStoreLogger(DataStore)
        :return: An instance of DataStoreLogger
        """
        return DataStoreLogger(self)

    def _remove_profile_from_device(self, device_list):
        if device_list is None:
            return None
        if not isinstance(device_list, list):
            device_list = [device_list]

        for index, device in enumerate(device_list):
            profile_name = device.get("profile_name")
            if profile_name is None:
                continue

            profile = self.profile_get(profile_name)
            if profile is None or len(profile) != 1:
                continue
            profile = profile[0]

            for key in profile:
                device_key_value = device.get(key, None)
                profile_key_value = profile.get(key, None)
                if device_key_value == profile_key_value:
                    device_list[index].pop(key)

        return device_list

    # CANNED QUERIES
    def get_node(self, device_name=None):
        """

        :param device_name: As explained in DataStore.device_get()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("node", device_name)

    def get_bmc(self, device_name=None):
        """

        :param device_name: As explained in DataStore.device_get()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("bmc", device_name)

    def get_pdu(self, device_name=None):
        """

        :param device_name: As explained in DataStore.device_get()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("pdu", device_name)

    def get_psu(self, device_name=None):
        """
        :param device_name: As explained in DataStore.device_get()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("psu", device_name)

    def get_devices_by_type(self, device_type, device_name=None):
        """
        Filter the list of devices by type. The implementation here pulls all devices then filters, you can probably
        do this faster in the database or something, so feel free to override this method!
        :param device_type:
        :param device_name: As explained in DataStore.device_get()
        :return: A list (possibly empty) of devices filtered by device_type
        """
        devices = self.device_get(device_name)
        filtered_devices = list()
        if devices is None:
            return filtered_devices
        for device in devices:
            if device.get("device_type") == device_type:
                filtered_devices.append(device)

        return filtered_devices

    def get_profile_devices(self, profile_name):
        """
        A list of devices that have a given profile. This is implemented in DataStore, but will probably be faster
        in a database or something, so feel free to override it!
        :param profile_name:
        :return:
        """
        devices = self.device_get()
        filtered_devices = list()
        if devices is None:
            return filtered_devices
        for device in devices:
            if device.get("profile_name") == profile_name:
                filtered_devices.append(device)

        return filtered_devices


class DataStoreException(Exception):
    """
    A staple Exception thrown by the DataStore
    """
    def __init__(self, msg):
        super(DataStoreException, self).__init__()
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class DataStoreLogger(object):
    """
    Following the logging interface, so that we don't have to change code to use a traditional logger or a
    datastore logger.
    """

    def __init__(self, datastore):
        self.ds = datastore

    def critical(self, log_msg, device_name=None, process=None):
        """A serious problem, indication that the program itself may be unable
           to continue."""
        self.ds.log_add(logging.CRITICAL, log_msg, device_name, process)

    def error(self, log_msg, device_name=None, process=None):
        """Due to a more serious problem, the software has not been able to
           perform some function."""
        self.ds.log_add(logging.ERROR, log_msg, device_name, process)

    def journal(self, command, command_result=None):
        """ Logs the user's transactions, where transaction is the command
            isued by the user"""
        # TODO: Make journal logging great again!
        start_msg = "Job Started"
        cmd_name = command.get_name()
        journal_args = {
            'cmd': cmd_name,
            'device': command.device_name,
            'cmdargs': ''.join(command.command_args)
        }

        msg = start_msg if command_result is None else command_result.message
        msg += " {}".format(journal_args)
        self.ds.log_add(self.ds.JOURNAL, msg)

    def warning(self, log_msg, device_name=None, process=None):
        """An indication that something unexpected happened, or indicative of
           some problem in the near future. The software is still working as
           expected."""
        self.ds.log_add(logging.WARNING, log_msg, device_name, process)

    def info(self, log_msg, device_name=None, process=None):
        """Confirmation that things are working as expected."""
        self.ds.log_add(logging.INFO, log_msg, device_name, process)

    def debug(self, log_msg, device_name=None, process=None):
        """Detailed information, typically of interest only when diagnosing
           problems."""
        self.ds.log_add(logging.DEBUG, log_msg, device_name, process)


def get_ctrl_logger():
    return logging.getLogger('DataStore')