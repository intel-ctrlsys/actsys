# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 <company or person>
#
import unittest
import subprocess
import os
from actsys import StartExample


class TestStarter(unittest.TestCase):

    def setUp(self):
        self.command = ['actsys']

    def test_run(self):
        pipe = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pipe.communicate()
        print(stdout)
        self.assertEquals(stdout.splitlines(), "Version: 0.1.0\nHello World!\n".splitlines())
