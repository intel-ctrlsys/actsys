# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Interface and Classes for using the DataStore
"""
import logging
from logging import StreamHandler
from abc import ABCMeta, abstractmethod
from ClusterShell.NodeSet import NodeSet, std_group_resolver, set_std_group_resolver, fold, NodeSetParseError
from ClusterShell.NodeUtils import GroupSource, GroupResolver, GroupResolverConfig


class DataStoreGroupSource(GroupSource):
    def __init__(self, name, datastore, groups=None, allgroups=None):
        super(DataStoreGroupSource, self).__init__(name, groups, allgroups)
        self.datastore = datastore

    def resolv_map(self, group):
        return self.datastore.get_group_devices(group)

    def resolv_list(self):
        return self.datastore.list_groups()


class DataStore(object):
    """
    Data Store interface.
    """
    __metaclass__ = ABCMeta
    LOG_FORMAT = "%(asctime)s / %(levelname)s / %(name)s / %(device_name)s / %(message)s"
    LOG_LEVEL = logging.DEBUG

    LOG_LEVEL_CRITICAL = logging.CRITICAL
    LOG_LEVEL_FATAL = LOG_LEVEL_CRITICAL
    LOG_LEVEL_ERROR = logging.ERROR
    LOG_LEVEL_WARNING = logging.WARNING
    LOG_LEVEL_WARN = LOG_LEVEL_WARNING
    LOG_LEVEL_INFO = logging.INFO
    LOG_LEVEL_JOURNAL = 15
    LOG_LEVEL_DEBUG = logging.DEBUG

    DeviceListParseError = NodeSetParseError

    def __init__(self):
        self.logger = get_logger()
        self.datastore_group_resolver = self._setup_group_config()

    def _setup_group_config(self):
        datastore_group_resolver = GroupResolver(default_source=DataStoreGroupSource("DataStoreSource", self))
        set_std_group_resolver(datastore_group_resolver)
        return datastore_group_resolver


    @abstractmethod
    def get_device(self, device_name):
        """
        Returns the first device found or None.
        :param device_name: Either the device_id, hostname or ip_address of the device you are looking for. (In that
            priority order)
        :return:
        """
        self.logger.debug("DataStore.get_device called", device_name=device_name)

    @abstractmethod
    def list_devices(self, filters=None):
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
        self.logger.debug("DataStore.list_devices called with filters {}".format(filters))
        return list()

    @abstractmethod
    def set_device(self, device_info_list):
        """
        Either updates or creates a device. This device is saved to the DataStore. An update is attempted when device_id
         is passed in via the device_info param. Otherwise, the device is created.
        :param device_info_list: An object or dict of values that define the device. The only required value is that of device_type.
        :return list: the affected device_id(s)
        :raise DataStoreException when device_type is not set in the device_info param
        """
        self.logger.debug("DataStore.set_device called: {}".format(device_info_list))
        if not isinstance(device_info_list, list):
            device_info_list = [device_info_list]

        for device_info in device_info_list:
            if device_info.get("device_type") is None:
                raise DataStoreException("device_type is a required key/value in the device_info field")

            profile_name = device_info.get("profile_name")
            if profile_name is not None:
                profile_names = self.get_profile_names()
                if profile_name not in profile_names:
                    raise DataStoreException("Cannot set device with profile '{}', because that profile "
                                             "does not exist.".format(profile_name))

    @abstractmethod
    def delete_device(self, device_list):
        """
        Remove the device. Be very careful.
        :param device_list: As explained in DataStore.get_device()@device_name, optionally accepts a list of device_names.
        :return: a list of deleted device_id's of the affected device(s)
        """
        self.logger.debug("DataStore.delete_device called", device_name=device_list)

    @abstractmethod
    def get_device_history(self, device_name=None):
        """

        :param device_name:
        :return:
        """
        self.logger.debug("DataStore.get_device_history called", device_name=device_name)

    @abstractmethod
    def get_profile(self, profile_name):
        """
        Get the first profile foudn that matches the specified profile_name.
        :param profile_name:  unique id and reference name of this profile
        :return: A single profile of type dict()
        """
        self.logger.debug("DataStore.get_profile called: {}".format(profile_name))

    def get_profile_names(self):
        profiles = self.list_profiles()
        return map(lambda x: x.get("profile_name"), profiles)

    @abstractmethod
    def list_profiles(self, filters=None):
        """
        Get profiles. Filtered by profile name, if specified.
        :param profile_name: unique id and reference name of this profile
        :return: A List of profiles
        """
        self.logger.debug("DataStore.list_profiles called: %s", filters)
        return list()

    @abstractmethod
    def set_profile(self, profile_info):
        """
        Either updates or creates a profile. This is saved to the DataStore. An update occurs when the profile_info
        param has a profile_name that already exists.
        :param profile_info: An object or dict of properties to be contained in this profile. profile_name must be
            included in this object/dict
        :return: profile_name
        :raise DataStoreException if profile_name is not set in profile info.
        """
        self.logger.debug("DataStore.set_profile called: {}".format(profile_info))
        if profile_info.get("profile_name") is None:
            raise DataStoreException("Cannot upsert, profile_name must be specified")
        return profile_info.get("profile_name")

    @abstractmethod
    def delete_profile(self, profile_name):
        """
        Attempts to remove a profile. This cannot be done if the profile is in use
        by any other devices.
        :param profile_name: As explained in list_profiles()
        :return: profile_name
        :raise DataStoreException if the profile cannot be delete because it is in use by devices.
        """
        self.logger.debug("DataStore.delete_profile called: {}".format(profile_name))
        devices_using_profile = self.get_profile_devices(profile_name)
        if len(devices_using_profile) != 0:
            raise DataStoreException("The profile '{}' cannot be deleted because it is in use by the following devices:"
                                     "{}".format(profile_name, devices_using_profile))
        return profile_name

    @abstractmethod
    def list_logs(self, device_name=None, limit=100):
        """
        If no device_name is specified, returns general logs.
        If device_name is specified, returns device logs.

        :param device_name: As explained in DataStore.list_devices()
        :param limit: how many logs are returned?
        :return: A list of Logs
        """
        self.logger.debug("DataStore.list_logs called", device_name=device_name)

    @abstractmethod
    def list_logs_between_timeslice(self, begin, end, device_name=None, limit=100):
        """

        :param begin: datetime
        :param end: datetime
        :param device_name: As explained in DataStore.list_devices()
        :param limit: how many logs to return
        :return: A list of logs
        """
        self.logger.debug("DataStore.list_logs_between_timeslice: Between {} and {}".format(begin, end),
                          device_name=device_name)

    @abstractmethod
    def add_log(self, level, msg, device_name=None, process=None):
        """
        Add a log to the datastore.
        :param level: Per spec https://docs.python.org/2/library/logging.html#logging-levels
            with the additional log level of JOURNAL
        :param process:
        :param msg:
        :param device_name: As explained in DataStore.list_devices()
        :return: None
        :raise DataStore Expection if the level is not a valid log level as sepecified in
            Datastore.get_log_levels()
        """
        if level not in self.get_log_levels():
            raise DataStoreException("Invalid log level specified. Please use the appropriate level as determined"
                                     "in Datastore.get_log_levels()")

    @abstractmethod
    def get_configuration_value(self, key):
        """
        Get the value for a particular key in the configuration
        :param key: str
        :return: value: str or None if the key is not found
        """
        self.logger.debug("DataStore.get_configuration_value called: {}".format(key))

    @abstractmethod
    def list_configuration(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def set_configuration(self, key, value):
        """
        Insert the new configuration value, update on key conflict
        :param key: str
        :param value: str
        :return: key
        """
        self.logger.debug("DataStore.set_configuration called: {} / {}".format(key, value))

    @abstractmethod
    def delete_configuration(self, key):
        """
        Delete the value of a given key
        :param key: str
        :return: value: str or None if nothing was deleted.
        """
        self.logger.debug("DataStore.delete_configuration called: {}".format(key))

    @abstractmethod
    def list_groups(self):
        """
        List the groups known.
        For example:
            $ ... group list
            @all
            @sms
            @compute
            @gpu
        :return:
        """
        pass

    @abstractmethod
    def get_group_devices(self, group):
        """
        List all devices that belong to a group.
        For example:
            $ ... group list @compute
            c[1-20]
        :param group:
        :return:
        """
        pass

    def get_device_groups(self, device_list):
        """
        For example:
            $ ... device groups c1
            @all
            @compute
        :param device_list:
        :return:
        """
        groups = self.list_groups()
        device_in_groups = list()
        for group in groups.keys():
            ns = NodeSet(groups.get(group, []))
            if device_list in ns:
                device_in_groups.append(group)

        # return [group for group in groups.keys() if device in groups.get(group, [])]
        return device_in_groups

    @abstractmethod
    def add_to_group(self, device_list, group):
        """
        Adds the given devices/groups to the group. Creates a group if necessary.
        :param device_list:
        :param group:
        :return:
        """
        pass

    @abstractmethod
    def remove_from_group(self, device_list, group):
        """
        Removes the given devices/groups from the group. Deletes the group if empty.
        :param device_list:
        :param group:
        :return:
        """
        pass

    def expand_device_list(self, device_list):
        """
        Expand strings like "device[1-3]" into lists like ["device1", "device2", device3"].
        Also handles groups like "@compute_nodes".
        See the range of inputs at: http://clustershell.readthedocs.io/en/latest/tools/nodeset.html
        :param device_list: A list of devices.
        :raise DevicelListParseError: When the expression is not parsable.
        :return:
        """
        return list(NodeSet(device_list, resolver=self.datastore_group_resolver))

    @staticmethod
    def fold_devices(device_list):
        """
        Collabse/fold hte given devicelist to the smallest possible one.
        :param device_list:
        :return:
        """
        if isinstance(device_list, list):
            device_list = ",".join(device_list)
        return fold(device_list)

    # UTIL FUNCTIONS
    def get_device_types(self):
        """
        Get the device types that the DataStore knows about.
        :return:
        """
        devices = self.list_devices()
        types = list()

        for device in devices:
            device_type = device.get("device_type")
            if device_type is not None and device_type not in types:
                types.append(device_type)

        return types

    @classmethod
    def get_log_levels(cls):
        """
        Get the log levels that the DataStore knows about.
        :return:
        """
        return [
            cls.LOG_LEVEL_CRITICAL,
            cls.LOG_LEVEL_ERROR,
            cls.LOG_LEVEL_WARNING,
            cls.LOG_LEVEL_INFO,
            cls.LOG_LEVEL_JOURNAL,
            cls.LOG_LEVEL_DEBUG
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
            # Get the passed in profile name
            profile_name = device.get("profile_name")
            if profile_name is None:
                # Attempt to get it from the DB. This is so that if we are deleting the profile_name, we remove profile
                #  elements too.
                db_device = self.get_device(device.get("hostname"))
                if db_device is not None:
                    profile_name = db_device.get("profile_name")
                if profile_name is None:
                    # No profile specified here or in the DB, nothing to do.
                    continue

            profile = self.get_profile(profile_name)
            if profile is None:
                continue

            for key in profile.keys():
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

        :param device_name: As explained in DataStore.list_devices()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("node", device_name)

    def get_bmc(self, device_name=None):
        """

        :param device_name: As explained in DataStore.list_devices()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("bmc", device_name)

    def get_pdus_for_device(self, device_name):
        """
        Get any PDUs attached to this device
        :param device_name:
        :return:
        """
        raise NotImplementedError()

    def get_pdu(self, device_name=None):
        """

        :param device_name: As explained in DataStore.list_devices()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("pdu", device_name)

    def get_psu(self, device_name=None):
        """
        :param device_name: As explained in DataStore.list_devices()
        :return: A list (possibly empty) of devices filtered by device_type == 'pdu'
        """
        return self.get_devices_by_type("psu", device_name)

    def get_devices_by_type(self, device_type, device_name=None):
        """
        Filter the list of devices by type. The implementation here pulls all devices then filters, you can probably
        do this faster in the database or something, so feel free to override this method!
        :param device_type:
        :param device_name: As explained in DataStore.list_devices()
        :return: A list (possibly empty) of devices filtered by device_type
        """
        if device_name is None:
            devices = self.list_devices()
        else:
            devices = [self.get_device(device_name)]
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
        devices = self.list_devices()
        filtered_devices = list()
        for device in devices:
            if device.get("profile_name") == profile_name:
                filtered_devices.append(device)

        return filtered_devices

    @abstractmethod
    def export_to_file(self, file_location):
        """
        Export the current config to a file location. This export includes:
            - devices
            - profiles
            - config
        It does not include:
            - device history
            - logs

        :param file_location: file location for the new file to go
        :return: Nothing
        """
        pass

    @abstractmethod
    def import_from_file(self, file_location):
        """
        Import from a valid configuration file. See self.export_to_file, this does not import logs or device_history.

        :param file_location:
        :return:
        :raise: When the file is not found
        """
        pass


class DataStoreException(Exception):
    """
    A staple Exception thrown by the DataStore
    """

    def __init__(self, message):
        super(DataStoreException, self).__init__()
        self.message = message

    def __str__(self):
        return repr(self.message)


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

        # self.ds.add_log(self.ds.JOURNAL, msg, device_name, "Journal")
        super(DataStoreLogger, self).log(DataStore.LOG_LEVEL_JOURNAL, msg, extra={
            "device_name": device_name
        }, *args, **kwargs)

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
            }, *args, **kwargs)

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
    """
    Return the logger used by the DataStore
    :return:
    """
    logging.setLoggerClass(DataStoreLogger)
    logger = logging.getLogger("Datastore")
    logger.setLevel(DataStore.LOG_LEVEL)
    logger.propagate = False
    return logger


def add_stream_logger(logger=None, log_level=None, log_format=None):
    """
    Add a Stream logger to print log msg's to the screen (std err).
    :param logger:
    :param log_level:
    :param log_format:
    :return:
    """
    if log_level is None:
        log_level = DataStore.LOG_LEVEL
    if log_format is None:
        log_format = DataStore.LOG_FORMAT
    if logger is None:
        logger = get_logger()

    stream_handler = None
    for handler in logger.handlers:
        if type(handler) == StreamHandler:
            stream_handler = handler

    if stream_handler is None:
        stream_handler = StreamHandler()

    formatter = logging.Formatter(log_format)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
