# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the NC API class
"""
from __future__ import print_function
import unittest
import tempfile
import os
import json
from mock import patch
from ..nc_api import NodeController

class TestUtilities(unittest.TestCase):
    def setUp(self):
        pass

    def test_existance(self):
        nc = NodeController('foo')
        self.assertIsNotNone(nc)
