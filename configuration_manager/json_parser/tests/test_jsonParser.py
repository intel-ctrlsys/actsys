# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
from unittest import TestCase

from ctrl.configuration_manager.json_parser.json_parser import JsonParser


class TestJsonParser(TestCase):
    def test_read_file(self):
        parser = JsonParser()
        data_content = parser.read_file('configuration_manager/json_parser/tests/file.json')
        self.assertIsNotNone(data_content)
        self.assertIsNotNone(parser.get_file_content_string(data_content))

    def test_read_file_non_existent_file(self):
        parser = JsonParser()
        self.assertIsNone(parser.read_file('unexistent_file.json'))

    def test_read_file_non_parsable(self):
        parser = JsonParser()
        self.assertIsNone(parser.read_file('test_jsonParser.py'))
