# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Common utilities that DataStore users or implementers need.
"""
import json
from os import linesep
from ClusterShell.NodeSet import expand, fold, grouplist, NodeSetParseError


class DeviceUtilities(object):
    """
    Utilities for handling device names and sets.
    """
    DeviceListParseError = NodeSetParseError

    @staticmethod
    def expand_devicelist(devicelist):
        """
        Expand strings like "device[1-3]" into lists like ["device1", "device2", device3"].
        Also handles groups like "@compute_nodes".
        See the range of inputs at: http://clustershell.readthedocs.io/en/latest/tools/nodeset.html
        :param devicelist: A list of devices.
        :raise DevicelListParseError: When the expression is not parsable.
        :return:
        """
        return expand(devicelist)

    @staticmethod
    def fold_devices(devicelist):
        """
        Collabse/fold hte given devicelist to the smallest possible one.
        :param device:
        :return:
        """
        if isinstance(devicelist, list):
            devicelist = ",".join(devicelist)
        return fold(devicelist)

    @staticmethod
    def get_groups():
        """
        List the known groups
        :return: A list of strings (group names)
        """
        return grouplist()


class DataStoreUtilities(object):
    """
    Handy utilities that everyone needs.
    """
    LINE_DELIMITER = ';;' + linesep

    @staticmethod
    def tail_file(filename, lines, formatter=None, log_filter=None):
        """
        Tries to emulate the function of tail on linux machines by retrieving the last x lines from a file.
        Allows for two functions, a formatter and lo_filter to be passed in for advanced usage.
        :param filename:
        :param lines:
        :param formatter:
        :param log_filter:
        :return:
        """
        num_lines = int(lines)

        with open(filename) as opened_file:
            content = opened_file.read().split(DataStoreUtilities.LINE_DELIMITER)

        # delete the empty element introduced by the split function
        content = filter(None, content)
        count = len(content)

        # Handle case when limit is larger than count
        if num_lines >= count:
            num_lines = count

        lines = list()
        i = count - 1
        while i >= 0 and len(lines) < num_lines:
            line = content[i]
            if formatter is not None:
                line = formatter(line)
            if log_filter is not None:
                if log_filter(line):
                    lines.append(line)
            else:
                lines.append(line)
            i -= 1

        lines.reverse()
        return lines

    @staticmethod
    def filter_dict(list_to_filter, filters):
        """
            Retrieve all devices from self.list_devices and filter them out according to the param filters. All entries
            in filter must be satisfied in order to be included in the filter list. In other words:
                device_included = device[key] = filter[0][key]
                                                AND device[key] == filter[1][key]
                                                ... AND device[key] == filter[n][key]
        :param filters: dict of key value pairs that a device must match.
        :return: A list
        """
        if filters is None:
            return list_to_filter
        filtered_objs = list()
        passed_filters = True
        for obj in list_to_filter:
            passed_filters = True
            for specified_filter in filters:
                passed_filters = passed_filters and obj.get(specified_filter) == filters.get(specified_filter)
            if passed_filters:
                filtered_objs.append(obj)

        return filtered_objs


class JsonParser(object):
    """Class to parse a Json file"""

    @staticmethod
    def read_file(file_path):
        """Read a Json file
        :rtype: dict
        :param file_name: File to parse
        :return: a map with the raw data from the json file
        """
        file_content = None
        try:
            with open(file_path) as data_file:
                file_content = json.load(data_file)
        except IOError:
            raise FileNotFound(file_path)
        except ValueError:
            raise NonParsableFile(file_path)
        return file_content

    @staticmethod
    def write_file(file_path, content):
        """
        Tries to format the content into JSON and put it in a file at the file_path.
        :param file_path: str
        :param content: str
        :return:
        """
        try:
            with open(file_path, "w") as json_file:
                json_file.write(json.dumps(content, sort_keys=True, indent=2, separators=(',', ': ')))
        except IOError as io_error:
            print(io_error)
            raise FileNotFound(file_path)
        except ValueError:
            raise NonParsableFile(file_path)

    @staticmethod
    def get_file_content_string(file_content):
        """ This method allows to get a human readable abtraction of a dict
        :rtype: str
        :param file_content: dict
        :return: string with a readable representation of the data
        """
        return json.dumps(file_content, sort_keys=True, indent=2, separators=(',', ': '))


class FileNotFound(Exception):
    """ File not found exception """

    def __init__(self, file_path):
        super(FileNotFound, self).__init__()
        self.value = "File {0} not found.".format(file_path)

    def __str__(self):
        return repr(self.value)


class NonParsableFile(Exception):
    """ Non parsable file exception"""

    def __init__(self, file_path):
        super(NonParsableFile, self).__init__()
        self.value = "File {0} cannot be parsed.".format(file_path)

    def __str__(self):
        return repr(self.value)
