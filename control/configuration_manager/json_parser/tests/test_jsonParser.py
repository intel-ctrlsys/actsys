# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
from unittest import TestCase

from ..json_parser import JsonParser, FileNotFound, NonParsableFile
from ...tests.test_json_files import TestJsonFiles


class TestJsonParser(TestCase):
    def test_read_file(self):
        parser = JsonParser()
        TestJsonFiles.write_file('file.json')
        data_content = parser.read_file('file.json')
        TestJsonFiles.remove_file('file.json')
        self.assertIsNotNone(data_content)
        self.assertIsNotNone(parser.get_file_content_string(data_content))

    def test_read_file_non_existent_file(self):
        parser = JsonParser()
        self.assertRaises(FileNotFound, parser.read_file, 'unexistent_file.json')
        try:
            parser.read_file('unexistent_file.json')
        except FileNotFound as e:
            print e

    def test_read_file_non_parsable(self):
        parser = JsonParser()
        TestJsonFiles.write_file('non_parsable.json')
        self.assertRaises(NonParsableFile, parser.read_file, 'non_parsable.json')
        try:
            parser.read_file('non_parsable.json')
        except NonParsableFile as e:
            print e
        TestJsonFiles.remove_file('non_parsable.json')
