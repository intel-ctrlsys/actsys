# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Parser for json files
"""

import json


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
    def get_file_content_string(file_content):
        """ This method allows to get a human readable abtraction of a dict
        :rtype: str
        :param file_content: dict
        :return: string with a readable representation of the data
        """
        return json.dumps(file_content, indent=4, sort_keys=True)


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
