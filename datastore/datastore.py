# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
from __future__ import print_function
import logging
from logging import StreamHandler
from abc import ABCMeta, abstractmethod


class DataStore(object):
    """
    Data Store interface.
    """
    __metaclass__ = ABCMeta
    LOG_FORMAT = "%(asctime)s / %(levelname)s / %(name)s / %(device_name)s / %(message)s"
    LOG_LEVEL = logging.DEBUG
    LOG_LEVEL_JOURNAL = 15
    JOURNAL = 15

    def __init__(self, print_to_screen):
        self.print_to_screen = print_to_screen
        self.logger = get_logger()

        if self.print_to_screen is True:
            add_stream_logger(self.logger)

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
        self.logger.debug("DataStore.device_get called", device_name=device_name)
        return list()

    def device_list_filter(self, filters):
        """
            Retrieve all devices from self.device_get and filter them out according to the param filters. All entries
            in filter must be satisfied in order to be included in the filter list. In other words:
                device_included = device[key] = filter[0][key]
                                                AND device[key] == filter[1][key]
                                                ... AND device[key] == filter[n][key]
        :param filters: dict of key value pairs that a device must match.
        :return: A list
        """
        devices = self.device_get()
        self.logger.debug("device_list: Attempting to print all devices that have "
                          "the following attributes: {}".format(filters))

        filtered_devices = list()
        passed_filters = True
        for device in devices:
            passed_filters = True
            for specified_filter in filters:
                passed_filters = passed_filters and device.get(specified_filter) == filters.get(specified_filter)
            if passed_filters:
                filtered_devices.append(device)

        return filtered_devices

    @abstractmethod
    def device_upsert(self, device_info):
        """
        Either updates or creates a device. This device is saved to the DataStore. An update is attempted when device_id
         is passed in via the device_info param. Otherwise, the device is created.
        :param device_info: An object or dict of values that define the device. The only required value is that of device_type.
        :return: the affected device_id
        :raise DataStoreException when device_type is not set in the device_info param
        """
        self.logger.debug("DataStore.device_upsert called: {}".format(device_info))

        if device_info.get("device_type") is None:
            raise DataStoreException("device_type is a required key/value in the device_info field")

    @abstractmethod
    def device_logical_delete(self, device_name):
        """
        Logically removes a device from the system database. This device will remain in the database, but no longer
        be reachable via getters and setters. The purpose of this option is to allow data about old devices to
        persist for history's sake, but not be part of the system.
        :param device_name: As explained in DataStore.device_get()
        :return: device_id of the affected device or None
        """
        self.logger.debug("DataStore.device_logical_delete called", device_name=device_name)

    @abstractmethod
    def device_fatal_delete(self, device_name):
        """
        Remove the device, all logs, and SKUS associated with the device. Be very careful.
        :param device_name: As explained in DataStore.device_get()
        :return: device_id of the affected device or None
        """
        self.logger.debug("DataStore.device_fatal_delete called", device_name=device_name)

    @abstractmethod
    def profile_get(self, profile_name=None):
        """
        Get profiles. Filtered by profile name, if specified.
        :param profile_name: unique id and reference name of this profile
        :return: A List of profiles
        """
        self.logger.debug("DataStore.profile_get called: {}".format(profile_name))
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
        self.logger.debug("DataStore.profile_upsert called: {}".format(profile_info))
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
        self.logger.debug("DataStore.profile_delete called: {}".format(profile_name))
        devices_using_profile = self.get_profile_devices(profile_name)
        if len(devices_using_profile) != 0:
            raise DataStoreException("The profile '{}' cannot be deleted because it is in use by the following devices:"
                                     "{}". format(profile_name, devices_using_profile))
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
        self.logger.debug("DataStore.log_get called", device_name=device_name)

    @abstractmethod
    def log_get_timeslice(self, begin, end, device_name=None, limit=100):
        """

        :param begin: datetime
        :param end: datetime
        :param device_name: As explained in DataStore.device_get()
        :param limit: how many logs to return
        :return: A list of logs
        """
        self.logger.debug("DataStore.log_get_timeslice: Between {} and {}".format(begin, end), device_name=device_name)

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
        :raise DataStore Expection if the level is not a valid log level as sepecified in
            Datastore.get_log_levels()
        """
        if level not in self.get_log_levels():
            raise DataStoreException("Invalid log level specified. Please use the appropriate level as determined"
                                     "in Datastore.get_log_levels()")

    @abstractmethod
    def configuration_get(self, key):
        """
        Get the value for a particular key in the configuration
        :param key: str
        :return: value: str or None if the key is not found
        """
        self.logger.debug("DataStore.configuration_get called: {}".format(key))

    @abstractmethod
    def configuration_upsert(self, key, value):
        """
        Insert the new configuration value, update on key conflict
        :param key: str
        :param value: str
        :return: key
        """
        self.logger.debug("DataStore.configuration_upsert called: {} / {}".format(key, value))

    @abstractmethod
    def configuration_delete(self, key):
        """
        Delete the value of a given key
        :param key: str
        :return: value: str or None if nothing was deleted.
        """
        self.logger.debug("DataStore.configuration_delete called: {}".format(key))

    # UTIL FUNCTIONS
    def get_device_types(self):
        devices = self.device_get()
        types = list()

        for device in devices:
            device_type = device.get("device_type")
            if device_type is not None and device_type not in types:
                types.append(device_type)

        return types

    def get_log_levels(self):
        return [
            logging.CRITICAL,
            logging.ERROR,
            self.LOG_LEVEL_JOURNAL,
            logging.WARN,
            logging.INFO,
            logging.DEBUG,
            logging.NOTSET
        ]

    def get_logger(self):
        """
        The same as running DataStoreLogger(DataStore)
        :return: An instance of DataStoreLogger
        """
        return get_logger()

    def set_log_level(self, logging_level):
        """
        Set the level of the datastore and all of the handlers to the passed in level
        :param logging_level:
        :return:
        :raise: DataStoreExcpetion, if the passed in level is not in Datastore.get_log_levels()
        """
        if logging_level not in self.get_log_levels():
            raise DataStoreException("Cannot set the log level to something that is not in DataStore.get_log_levels()")

        DataStore.LOG_LEVEL = logging_level

        for handler in self.logger.handlers:
            handler.setLevel(logging_level)

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
                if key == "profile_name":
                    continue
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


class DataStoreLogger(logging.getLoggerClass()):
    """
    Following the logging interface, so that we don't have to change code to use a traditional logger or a
    datastore logger.
    """

    def __init__(self, name=None, level=logging.NOTSET):
        super(DataStoreLogger, self).__init__(name, level)
        logging.addLevelName(DataStore.LOG_LEVEL_JOURNAL, "JOURNAL")

    def critical(self, log_msg, device_name=None, *args, **kwargs):
        """A serious problem, indication that the program itself may be unable
           to continue."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(DataStoreLogger, self).critical(msg)
        else:
            super(DataStoreLogger, self).critical(log_msg, extra={
                "device_name": device_name,
            }, *args, **kwargs)

    def error(self, log_msg, device_name=None, *args, **kwargs):
        """Due to a more serious problem, the software has not been able to
           perform some function."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(DataStoreLogger, self).error(msg)
        else:
            super(DataStoreLogger, self).error(log_msg, extra={
                "device_name": device_name,
            }, *args, **kwargs)

    def journal(self, command_name, command_args=None, device_name=None, command_result=None, *args, **kwargs):
        """ Logs the user's transactions, where transaction is the command
            isued by the user"""
        if command_result is None:
            msg = "Command Started: ({}) Args: ({})".format(command_name, command_args, *args, **kwargs)
        else:
            msg = "Command Ended: ({}) Args: ({}) Result: {}".format(command_name, command_args, command_result)

        # self.ds.log_add(self.ds.JOURNAL, msg, device_name, "Journal")
        super(DataStoreLogger, self).log(DataStore.LOG_LEVEL_JOURNAL, msg, extra={
            "device_name": device_name
        },  *args, **kwargs)

    def warning(self, log_msg, device_name=None, *args, **kwargs):
        """An indication that something unexpected happened, or indicative of
           some problem in the near future. The software is still working as
           expected."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(DataStoreLogger, self).warning(msg)
        else:
            super(DataStoreLogger, self).warning(log_msg, extra={
                "device_name": device_name,
            },  *args, **kwargs)

    def info(self, log_msg, device_name=None, *args, **kwargs):
        """Confirmation that things are working as expected."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(DataStoreLogger, self).info(msg)
        else:
            super(DataStoreLogger, self).info(log_msg, extra={
                "device_name": device_name,
            }, *args, **kwargs)

    def debug(self, log_msg, device_name=None, *args, **kwargs):
        """Detailed information, typically of interest only when diagnosing
           problems."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(DataStoreLogger, self).debug(msg)
        else:
            super(DataStoreLogger, self).debug(log_msg, extra={
                "device_name": device_name,
            }, *args, **kwargs)


def get_logger():
    logging.setLoggerClass(DataStoreLogger)
    logger = logging.getLogger("DataStore")
    logger.setLevel(DataStore.LOG_LEVEL)
    return logger


def add_stream_logger(logger=None, log_level=DataStore.LOG_LEVEL, log_format=DataStore.LOG_FORMAT):
    stream_handler = None
    for handler in logger.handlers:
        if isinstance(handler, StreamHandler):
            stream_handler = handler

    if stream_handler is None:
        stream_handler = StreamHandler()

    formatter = logging.Formatter(log_format)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

