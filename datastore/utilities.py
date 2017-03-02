# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
import json


class DataStoreUtilities(object):

    @staticmethod
    def tail_file(filename, lines, formatter=None, log_filter=None):
        num_lines = int(lines)

        with open(filename) as f:
            content = f.read().splitlines()

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
        try:
            with open(file_path, "w") as json_file:
                json_file.write(json.dumps(content, sort_keys=True, indent=2, separators=(',', ': ')))
        except IOError as io:
            print(io)
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