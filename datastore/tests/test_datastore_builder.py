# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the FileStore class
"""
from __future__ import print_function
import unittest
import os
import tempfile
from mock import patch
from .. import DataStoreBuilder, DataStoreException, DataStore
from ..filestore import FileStore
from ..postgresstore import PostgresStore
from .. multistore import MultiStore


class TestDataStoreBuilder(unittest.TestCase):

    def setUp(self):
        self.dsb = DataStoreBuilder()

    def testinit(self):
        res = DataStoreBuilder()
        self.assertEqual(len(res.dbs), 0)

    def test_add_file_db(self):
        self.dsb.add_file_db("config-example.json")
        self.assertTrue(isinstance(self.dsb.dbs[0], FileStore))

    @patch("psycopg2.connect")
    def test_add_postgres_db(self, mock_connect):
        self.dsb.add_postgres_db("")
        self.assertTrue(isinstance(self.dsb.dbs[0], PostgresStore))

    @patch("psycopg2.connect")
    def test_set_print_to_screen(self, mock_connect):
        self.dsb.add_file_db("config-example.json")
        self.dsb.add_postgres_db("")
        self.dsb.set_print_to_screen(True)
        self.assertTrue(self.dsb.print_to_screen)
        self.assertTrue(self.dsb.dbs[0].print_to_screen)

    @patch("psycopg2.connect")
    def test_set_log_level(self, mock_connect):
        import logging

        self.dsb.add_file_db("config-example.json")
        self.dsb.add_postgres_db("")
        self.dsb.set_log_level(logging.INFO)

        self.assertEqual(self.dsb.log_level, logging.INFO)
        self.assertEqual(self.dsb.dbs[0].log_level, logging.INFO)

    @patch("psycopg2.connect")
    def test_build(self, mock_connect):
        self.dsb.add_file_db("config-example.json")
        filestore = self.dsb.build()
        self.assertTrue(isinstance(filestore, FileStore))

        self.dsb.add_postgres_db("")
        multistore = self.dsb.build()
        self.assertTrue(isinstance(multistore, MultiStore))

    def test_get_datastore_from_env_vars(self):
        with self.assertRaises(DataStoreException):
            DataStoreBuilder.get_datastore_from_env_vars()

        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write("{}")
        temp_file.close()
        os.environ["datastore_test_file_loc"] = temp_file.name
        result = DataStoreBuilder.get_datastore_from_env_vars(True, "datastore_test_file_loc")
        self.assertIsInstance(result, DataStore)
        self.assertIsInstance(result, FileStore)
        os.environ.pop("datastore_test_file_loc", None)
        os.remove(temp_file.name)


