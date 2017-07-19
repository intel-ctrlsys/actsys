# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 <company or person>
#
import unittest
from actsys import StartExample


class TestStarter(unittest.TestCase):

    def setUp(self):
        self.start_example = StartExample()

    def test_run(self):
        self.start_example.run()

    def test_version(self):
        self.start_example.print_version()
