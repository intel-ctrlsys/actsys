# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
import os
import logging
from logging.handlers import RotatingFileHandler
from dateutil.parser import parse as date_parse
from .datastore import DataStore, DataStoreException
from .utilities import DataStoreUtilities, JsonParser


class FileStore(DataStore):
    """
    The filestore retireves
    """
    # TODO: test device_id in inserts
    LOG_FORMAT = "%(asctime)s / %(levelname)s / %(name)s / %(message)s"
    DEVICE_KEY = "device"
    CONFIG_KEY = "configuration_variables"
    PROFILE_KEY = "profile"

    def __init__(self, location, log_level):
        super(FileStore, self).__init__()
        self.location = location
        # TODO: lock the file: http://stackoverflow.com/a/186464/1767377
        self.parsed_file = JsonParser.read_file(location)
        self._setup_file_logger(log_level)

    def _setup_file_logger(self, log_level):
        """
        Sets up the logger to log things. If no log location is given a log file is created in ~/datastore.log.
        :return:
        """
        if log_level is None:
            log_level = DataStore.LOG_LEVEL

        log_rotating_file_handler = None
        for handler in self.logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                log_rotating_file_handler = handler
                break

        formatter = logging.Formatter(self.LOG_FORMAT)

        if log_rotating_file_handler is None:
            log_file_path = self.configuration_get("log_file_path")
            if log_file_path is None:
                log_file_path = os.path.expanduser('~/datastore.log')
                self.configuration_upsert("log_file_path", log_file_path)
                if not os.path.isfile(log_file_path):
                    log_file = open(log_file_path, "w")
                    log_file.close()

            log_file_max_bytes = self.configuration_get("log_file_max_bytes")
            if log_file_max_bytes is None:
                log_file_max_bytes = 0

            log_rotating_file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=log_file_max_bytes
            )
            log_rotating_file_handler.setLevel(log_level)
            log_rotating_file_handler.setFormatter(formatter)

            self.logger.addHandler(log_rotating_file_handler)
        else:
            log_rotating_file_handler.setLevel(log_level)
            log_rotating_file_handler.setFormatter(formatter)

    def add_profile_to_device(self, device_list):
        if device_list is None:
            return None
        if not isinstance(device_list, list):
            device_list = [device_list]

        for index, device in enumerate(device_list):
            profile_name = device.get("profile_name", None)
            if profile_name is None:
                # Nothing to add or change!
                continue
            profile = self.profile_get(profile_name)[0]
            for key in profile:
                if device.get(key, None) is None:
                    device_list[index][key] = profile.get(key)
        return device_list

    def save_file(self):
        JsonParser.write_file(self.location, self.parsed_file)

    def device_get(self, device_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).device_get(device_name)
        devices = self.parsed_file.get(self.DEVICE_KEY, [])
        if device_name is None:
            devices = [device for device in devices if device.get("deleted", False) is False]
            return self.add_profile_to_device(devices)
        else:
            index, device = self._device_find(device_name, devices)
            if device is not None:
                return self.add_profile_to_device(device)
            else:
                return []

    @staticmethod
    def _device_find(device_name, devices, find_deleted=False):
        """
        Given a device name and a list of devices, locates the device in that list.
        :param device_name:
        :param devices:
        :return: The index and device (index, device) or (None, None) if they are not found.
        """
        # Check for a matching device_id
        for index, device in enumerate(devices):
            if device.get('device_id') == device_name:
                if find_deleted is True:
                    return index, device
                elif device.get("deleted") is not True:
                    return index, device
        # Check for hostname
        for index, device in enumerate(devices):
            if device.get('hostname') == device_name:
                if find_deleted is True:
                    return index, device
                elif device.get("deleted") is not True:
                    return index, device
        # Check for ip
        for index, device in enumerate(devices):
            if device.get('ip_address') == device_name:
                if find_deleted is True:
                    return index, device
                elif device.get("deleted") is not True:
                    return index, device

        return None, None

    def device_upsert(self, device_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).device_upsert(device_info)

        # Update
        devices = self.parsed_file.get(self.DEVICE_KEY, None)
        if devices is None:
            # No devices, but we are about to add one, so create them!
            self.parsed_file[self.DEVICE_KEY] = list()
            devices = self.parsed_file.get(self.DEVICE_KEY)

        device_name = device_info.get("device_id")
        highest_node_id = 0
        for index, device in enumerate(devices):
            device_id = device.get('device_id')
            if device_id > highest_node_id:
                highest_node_id = device_id
            if device_id == device_name:
                # Update the device with what was passed in
                devices[index] = self._remove_profile_from_device(device_info)[0]
                self.save_file()
                return device.get("device_id")

        # Set device id to the next aval one
        if device_info.get("device_id") is None:
            device_info["device_id"] = highest_node_id + 1

        # Insert device
        devices.append(self._remove_profile_from_device(device_info)[0])
        self.save_file()
        return device_info.get("device_id")

    def device_delete(self, device_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).device_delete(device_name)
        devices = self.parsed_file.get(self.DEVICE_KEY, [])

        index, device = self._device_find(device_name, devices, True)
        if index is not None:
            devices.pop(index)
            self.save_file()
            return device.get("device_id")
        else:
            return None

    def device_history_get(self, device_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        raise DataStoreException("Not implemented for FileStore.")

    def profile_get(self, profile_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).profile_get(profile_name)
        profiles = self.parsed_file.get(self.PROFILE_KEY, [])
        if profile_name is None:
            return profiles
        else:
            for profile in profiles:
                if profile.get("profile_name") == profile_name:
                    return [profile]

            return []

    def profile_upsert(self, profile_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).profile_upsert(profile_info)
        profile_name = profile_info.get("profile_name")

        # Check for and update
        profiles = self.parsed_file.get(self.PROFILE_KEY)
        if profiles is None:
            # There are no profiles, but we are about to insert one. So create a profiles section.
            self.parsed_file[self.PROFILE_KEY] = list()
            profiles = self.parsed_file.get(self.PROFILE_KEY)

        for index, profile in enumerate(profiles):
            if profile_name == profile.get("profile_name"):
                profiles[index] = profile_info
                self.save_file()
                self.logger.info("DataStore.profile_delete result: Success, updated")
                return profile_name

        # Insert
        profiles.append(profile_info)
        self.save_file()
        self.logger.info("DataStore.profile_delete result: Success, inserted")
        return profile_name

    def profile_delete(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).profile_delete(profile_name)
        # TODO: check if the profile is in use, if it is, don't delete
        profiles = self.parsed_file.get(self.PROFILE_KEY, [])
        for index, profile in enumerate(profiles):
            if profile.get("profile_name") == profile_name:
                profiles.pop(index)
                self.save_file()
                self.logger.info("DataStore.profile_delete result: Success")
                return profile_name

        return None

    def log_get(self, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).log_get(device_name, limit)
        log_file = self.configuration_get("log_file_path")
        lines = DataStoreUtilities.tail_file(log_file, limit, self.log_formatter)
        self.logger.info("DataStore.log_get result: Returned {} lines".format(len(lines)))
        return lines

    @staticmethod
    def log_formatter(line):
        split = line.split(' / ')
        if len(split) == 4:
            return {
                # Other parsing options: http://stackoverflow.com/questions/466345/converting-string-into-datetime
                "timestamp": date_parse(split[0]),
                "level": logging.getLevelName(split[1]),
                "message": split[3],
                "process": split[2],
                "device_id": None,
            }
        elif len(split) == 6:
            return {
                # Other parsing options: http://stackoverflow.com/questions/466345/converting-string-into-datetime
                "timestamp": date_parse(split[0]),
                "level": logging.getLevelName(split[1]),
                "message": split[5],
                "process": split[3],
                "device_id": split[4],
            }
        else:
            raise RuntimeError("The logs in the log file are of an unknown format, cannot continue. "
                               "Line: {}".format(line))

    def log_get_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).log_get_timeslice(begin, end, device_name, limit)

        def time_filter(line):
            date = line.get("timestamp")
            return begin < date < end

        log_file = self.configuration_get("log_file_path")
        lines = DataStoreUtilities.tail_file(log_file, limit, self.log_formatter, time_filter)
        self.logger.info("DataStore.log_get result: Returned {} lines".format(len(lines)))
        return lines

    def log_add(self, level, msg, device_name=None, process=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).log_add(level, process, msg, device_name)
        # Get device id from device_name
        device_id = None
        device = self.device_get(device_name)
        if len(device) == 1:
            device_id = device[0].get("device_id", None)

        # log it
        msg = "{} / {} / ".format(process, device_id) + msg
        self.logger.log(level, msg)

    def configuration_get(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).configuration_get(key)
        result = self.parsed_file.get(self.CONFIG_KEY, {})
        result = result.get(key)
        self.logger.info("DataStore.configuration_get result: {}".format(result))
        return result

    def configuration_upsert(self, key, value):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).configuration_upsert(key, value)
        # check to make sure there is a configuration_varribles section... so we don't get a key_error
        if self.parsed_file.get(self.CONFIG_KEY) is None:
            self.parsed_file[self.CONFIG_KEY] = {}

        self.parsed_file[self.CONFIG_KEY][key] = value
        self.logger.info("DataStore.configuration_upsert result: Success")
        self.save_file()
        return key

    def configuration_delete(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).configuration_delete(key)
        if self.parsed_file.get(self.CONFIG_KEY) is None:
            return None
        popped_value = self.parsed_file[self.CONFIG_KEY].pop(key, None)
        self.logger.info("DataStore.configuration_delete result: Success")
        self.save_file()
        if popped_value is None:
            # Nothing was deleted...
            return None
        else:
            return key
