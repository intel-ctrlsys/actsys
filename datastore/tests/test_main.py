# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the main function
"""
from __future__ import print_function
import unittest
import os
import sys
import tempfile
from mock import patch
from .. import DataStoreBuilder, DataStoreException, DataStore
from ..__main__ import main


class TestMainFunction(unittest.TestCase):

    def setUp(self):
        self.dsb = DataStoreBuilder()

    def test_main_runs_DataStore(self):
        temp_db = tempfile.NamedTemporaryFile("w", delete=False)
        temp_db.close()
        old_env = os.environ.get("DATASTORE_LOCATION")
        os.environ["DATASTORE_LOCATION"] = temp_db.name
        sys.argv = ['datastore', 'device', 'list']

        with self.assertRaises(SystemExit):
            main()

        os.remove(temp_db.name)
        if old_env:
            os.environ["DATASTORE_LOCATION"] = old_env
