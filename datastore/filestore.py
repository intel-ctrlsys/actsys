# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
import os
import logging
import copy
from logging.handlers import RotatingFileHandler
from dateutil.parser import parse as date_parse
from pytz import UTC
from ClusterShell.NodeSet import NodeSet, RESOLVER_NOGROUP
from .datastore import DataStore, DataStoreException
from .utilities import DataStoreUtilities, JsonParser


class FileStore(DataStore):
    """
    The filestore retireves
    """
    # TODO: test device_id in inserts
    LOG_FORMAT = "%(asctime)s / %(levelname)s / %(name)s / %(message)s;;"
    DEVICE_KEY = "device"
    CONFIG_KEY = "configuration_variables"
    PROFILE_KEY = "profile"
    GROUPS_KEY = "groups"

    def __init__(self, location="/tmp/datastore_db", log_level=None):
        super(FileStore, self).__init__()
        self.location = location
        self.log_level = log_level if log_level is not None else DataStore.LOG_LEVEL
        # TODO: lock the file: http://stackoverflow.com/a/186464/1767377
        # If the file doesn't exist or is empty. Create it.
        try:
            if not os.path.isfile(location) or os.stat(location).st_size == 0:
                with open(location, "w") as f:
                    f.write("{}")
        except IOError:
            raise DataStoreException("Could not write to location {}. Do you have write permissions?".format(location))

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
            log_file_path = self.get_configuration_value("log_file_path")
            if log_file_path is None:
                log_file_path = '/tmp/datastore.log'
                self.set_configuration("log_file_path", log_file_path)
                if not os.path.isfile(log_file_path):
                    log_file = open(log_file_path, "w")
                    log_file.close()

            log_file_max_bytes = self.get_configuration_value("log_file_max_bytes")
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
            profile = self.get_profile(profile_name)
            if profile is None:
                # no valid profile, likely this is caused by an error in the config
                self.logger.warning("Device {}, has an invalid profile {}. Skipping for now, but this is likely due to"
                                    " an invalid configuration.".format(device.get("device_id"), profile_name))
                continue
            for key in profile:
                if device.get(key, None) is None:
                    device_list[index][key] = profile.get(key)
        return device_list

    def save_file(self, location=None):
        if location is None:
            location = self.location
        JsonParser.write_file(location, self.parsed_file)

    def get_device(self, device_name):
        devices = self.parsed_file.get(self.DEVICE_KEY, [])
        index, device = self._device_find(device_name, devices)
        if device is not None:
            return copy.copy(self.add_profile_to_device(device)[0])
        else:
            return None

    def list_devices(self, filters=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).list_devices(filters)
        devices = self.parsed_file.get(self.DEVICE_KEY, [])
        return DataStoreUtilities.filter_dict(self.add_profile_to_device(devices), filters)

    @staticmethod
    def _device_find(device_name, devices):
        """
        Given a device name and a list of devices, locates the device in that list.
        :param device_name:
        :param devices:
        :return: The index and device (index, device) or (None, None) if they are not found.
        """
        # Check for a matching device_id
        for index, device in enumerate(devices):
            if device.get('device_id') == device_name:
                return index, device
        # Check for hostname
        for index, device in enumerate(devices):
            if device.get('hostname') == device_name:
                return index, device
        # Check for ip
        for index, device in enumerate(devices):
            if device.get('ip_address') == device_name:
                return index, device

        return None, None

    def set_device(self, device_info_list):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).set_device(device_info_list)

        if not isinstance(device_info_list, list):
            device_info_list = [device_info_list]

        set_ids = list()
        # Update
        devices = self.parsed_file.get(self.DEVICE_KEY, None)
        if devices is None:
            # No devices, but we are about to add one, so create them!
            self.parsed_file[self.DEVICE_KEY] = list()
            devices = self.parsed_file.get(self.DEVICE_KEY)

        highest_node_id = 0
        for device_info in device_info_list:
            device_to_update_id = device_info.get("device_id")
            updated = False
            for index, device in enumerate(devices):
                device_id = device.get('device_id')
                if device_id > highest_node_id:
                    highest_node_id = device_id
                if device_id == device_to_update_id:
                    # Update the device with what was passed in
                    devices[index] = self._remove_profile_from_device(device_info)[0]
                    set_ids.append(device_info.get("device_id"))
                    updated = True
                    break

            if not updated:
                # Set device id to the next aval one
                if device_info.get("device_id") is None:
                    highest_node_id = highest_node_id + 1
                    device_info["device_id"] = highest_node_id

                # Insert device
                devices.append(self._remove_profile_from_device(device_info)[0])
                set_ids.append(device_info.get("device_id"))

        self.save_file()
        return set_ids

    def delete_device(self, device_list):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).delete_device(device_list)
        devices = self.parsed_file.get(self.DEVICE_KEY, [])

        if not isinstance(device_list, list):
            device_list = [device_list]

        deleted_device_ids = list()
        for device_name in device_list:
            index, device = self._device_find(device_name, devices)
            if index is not None:
                removed_device = devices.pop(index)
                self.save_file()
                deleted_device_ids.append(removed_device.get("device_id"))

        return deleted_device_ids

    def get_device_history(self, device_name=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        raise DataStoreException("Not implemented for FileStore.")

    def get_profile(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        profiles = self.parsed_file.get(self.PROFILE_KEY, [])
        for profile in profiles:
            if profile.get("profile_name") == profile_name:
                return profile

        return None

    def list_profiles(self, filters=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).list_profiles(filters)
        profiles = self.parsed_file.get(self.PROFILE_KEY, [])
        return DataStoreUtilities.filter_dict(profiles, filters)

    def set_profile(self, profile_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).set_profile(profile_info)
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
                self.logger.info("DataStore.delete_profile result: Success, updated")
                return profile_name

        # Insert
        profiles.append(profile_info)
        self.save_file()
        self.logger.info("DataStore.delete_profile result: Success, inserted")
        return profile_name

    def delete_profile(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).delete_profile(profile_name)
        # TODO: check if the profile is in use, if it is, don't delete
        profiles = self.parsed_file.get(self.PROFILE_KEY, [])
        for index, profile in enumerate(profiles):
            if profile.get("profile_name") == profile_name:
                profiles.pop(index)
                self.save_file()
                self.logger.info("DataStore.delete_profile result: Success")
                return profile_name

        return None

    def list_logs(self, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).list_logs(device_name, limit)
        log_file = self.get_configuration_value("log_file_path")
        lines = DataStoreUtilities.tail_file(log_file, limit, self.log_formatter)
        self.logger.info("DataStore.list_logs result: Returned {} lines".format(len(lines)))
        return lines

    @staticmethod
    def log_formatter(line):
        split = line.split(' / ')
        if len(split) == 4:
            return {
                # Other parsing options: http://stackoverflow.com/questions/466345/converting-string-into-datetime
                #
                "timestamp": date_parse(split[0] + "+00"),
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

    def list_logs_between_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).list_logs_between_timeslice(begin, end, device_name, limit)

        def time_filter(line):
            date = line.get("timestamp")
            return begin < date.replace(tzinfo=UTC) < end

        log_file = self.get_configuration_value("log_file_path")
        lines = DataStoreUtilities.tail_file(log_file, limit, self.log_formatter, time_filter)
        self.logger.info("DataStore.list_logs result: Returned {} lines".format(len(lines)))
        return lines

    def add_log(self, level, msg, device_name=None, process=None):
        """
        See @DataStore for function description. Only implementation details here.

        Log Add doesn't allow newlines in its implemntation.
        """
        super(FileStore, self).add_log(level, process, msg, device_name)
        # Get device id from device_name
        device_id = None
        device = self.get_device(device_name)
        if device is not None:
            device_id = device.get("device_id", None)

        # log it
        msg = "{} / {} / ".format(process, device_id) + msg.replace(os.linesep, ' ').replace('\n', ' ')
        self.logger.log(level, msg)

    def get_configuration_value(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).get_configuration_value(key)
        result = self.parsed_file.get(self.CONFIG_KEY, {})
        result = result.get(key)
        self.logger.info("DataStore.get_configuration_value result: {}".format(result))
        return result

    def list_configuration(self):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).list_configuration()
        result = list()
        config = self.parsed_file.get(self.CONFIG_KEY, {})
        for key in config.keys():
            result.append({"key": key, "value": config.get(key)})
        return result

    def set_configuration(self, key, value):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).set_configuration(key, value)
        # check to make sure there is a configuration_varribles section... so we don't get a key_error
        if self.parsed_file.get(self.CONFIG_KEY) is None:
            self.parsed_file[self.CONFIG_KEY] = {}

        self.parsed_file[self.CONFIG_KEY][key] = value
        self.logger.info("DataStore.set_configuration result: Success")
        self.save_file()
        return key

    def delete_configuration(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).delete_configuration(key)
        if self.parsed_file.get(self.CONFIG_KEY) is None:
            return None
        popped_value = self.parsed_file[self.CONFIG_KEY].pop(key, None)
        self.logger.info("DataStore.delete_configuration result: Success")
        self.save_file()
        if popped_value is None:
            # Nothing was deleted...
            return None
        else:
            return key

    def list_groups(self):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).list_groups()
        groups = self.parsed_file.get(self.GROUPS_KEY, {})
        return copy.copy(groups)

    def get_group_devices(self, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).get_group_devices(group)
        self.logger.debug("Getting for group: {}".format(group))
        groups = self.parsed_file.get(self.GROUPS_KEY, {})

        return copy.copy(str(groups.get(group, "")))

    def add_to_group(self, device_list, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).add_to_group(device_list, group)
        groups = self.parsed_file.get(self.GROUPS_KEY, None)
        if groups is None:
            self.parsed_file[self.GROUPS_KEY] = {}

        updated_device_set = NodeSet(self.parsed_file[self.GROUPS_KEY].get(group, None), resolver=RESOLVER_NOGROUP)
        device_list = super(FileStore, self).expand_device_list(device_list)
        updated_device_set.add(','.join(device_list))
        self.parsed_file[self.GROUPS_KEY][group] = str(updated_device_set)

        self.save_file()

        return updated_device_set

    def remove_from_group(self, device_list, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(FileStore, self).remove_from_group(device_list, group)
        groups = self.parsed_file.get(self.GROUPS_KEY, None)
        if groups is None:
            # Nothing to delete, done!
            return NodeSet()

        updated_device_set = NodeSet(self.parsed_file[self.GROUPS_KEY].get(group, None), resolver=RESOLVER_NOGROUP)
        updated_device_set.difference_update(device_list)
        if len(updated_device_set)  == 0 or device_list == '*':
            # Delete the group if its empty or user provided device_list is '*'
            self.parsed_file[self.GROUPS_KEY].pop(group, None)
            updated_device_set = NodeSet()
        else:
            # Modify the group, because its not empty yet.
            self.parsed_file[self.GROUPS_KEY][group] = str(updated_device_set)

        self.save_file()
        return updated_device_set

    def export_to_file(self, file_location):
        """
        See @DataStore for function description. Only implementation details here.

        Exporting is very simple for the file store, simply copy to current fileDB to another location.
        """
        self.save_file(file_location)

    def import_from_file(self, file_location):
        """
        See @DataStore for function description. Only implementation details here.

        Importing is very simple for the file store, simply copy to target file top the fileDB location and overwrite it
        """
        self.parsed_file = JsonParser.read_file(file_location)
        self._setup_file_logger(self.log_level)
        self.save_file()
