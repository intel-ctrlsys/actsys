# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the FileStore class
"""

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

        temp_file = tempfile.NamedTemporaryFile("w", delete=True)
        temp_file.close()
        self.dsb.add_file_db(temp_file.name)
        self.assertTrue(os.path.isfile(temp_file.name))
        os.remove(temp_file.name)

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

    @patch("psycopg2.connect")
    def test_set_default_log_level(self, mock_connect):
        import logging
        from datastore import get_logger
        from logging.handlers import RotatingFileHandler
        from datastore.postgresstore import PostgresLogHandler

        self.dsb.add_file_db("config-example.json", logging.CRITICAL)
        self.dsb.add_postgres_db("", logging.WARN)
        self.dsb.set_default_log_level(logging.INFO)
        self.assertEqual(DataStore.LOG_LEVEL, logging.INFO)
        logger = get_logger()
        fdbh = None
        pdbh = None
        for handler in logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                fdbh = handler
            if isinstance(handler, PostgresLogHandler):
                pdbh = handler
        self.assertEqual(fdbh.level, logging.CRITICAL)
        self.assertEqual(pdbh.level, logging.WARNING)

    @patch("psycopg2.connect")
    def test_set_default_log_level2(self, mock_connect):
        import logging
        from datastore import get_logger
        from logging.handlers import RotatingFileHandler
        from datastore.postgresstore import PostgresLogHandler

        self.dsb.set_default_log_level(logging.FATAL)
        self.assertEqual(DataStore.LOG_LEVEL, logging.FATAL)
        self.dsb.add_file_db("config-example.json", None)
        self.dsb.add_postgres_db("")

        logger = get_logger()
        fdbh = None
        pdbh = None
        for handler in logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                fdbh = handler
            if isinstance(handler, PostgresLogHandler):
                pdbh = handler
        self.assertEqual(fdbh.level, logging.FATAL)
        self.assertEqual(pdbh.level, logging.FATAL)

    @patch("psycopg2.connect")
    def test_build(self, mock_connect):
        self.dsb.add_file_db("config-example.json")
        filestore = self.dsb.build()
        self.assertTrue(isinstance(filestore, FileStore))

        self.dsb.add_postgres_db("")
        multistore = self.dsb.build()
        self.assertTrue(isinstance(multistore, MultiStore))

    def test_build_no_options(self):
        with self.assertRaises(DataStoreException):
            self.dsb.build()

    @patch.object(FileStore, "__init__")
    @patch.object(PostgresStore, "__init__")
    def test_get_datastore_from_string(self, mock_ps, mock_fs):
        mock_ps.return_value = None
        mock_fs.return_value = None

        with self.assertRaises(ValueError):
            DataStoreBuilder.get_datastore_from_string({})

        result = DataStoreBuilder.get_datastore_from_string("postgres://foo:bar")
        self.assertEqual(type(result), PostgresStore)

        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.close()
        result = DataStoreBuilder.get_datastore_from_string(temp_file.name)
        self.assertEqual(type(result), FileStore)
        os.remove(temp_file.name)

        result = DataStoreBuilder.get_datastore_from_string("garbage")
        self.assertEqual(type(result), PostgresStore)

        mock_ps.side_effect = Exception("Mocked exception")

        result = DataStoreBuilder.get_datastore_from_string(temp_file.name)
        self.assertEqual(type(result), FileStore)

        mock_fs.side_effect = [Exception("Mocked exception"), None]

        try:
            result = DataStoreBuilder.get_datastore_from_string(temp_file.name)
        except DataStoreException as dse:
            self.assertTrue(dse.message.startswith("The string '"), dse.message)

        mock_fs.side_effect = IOError("Insufficient permissions")
        try:
            result = DataStoreBuilder.get_datastore_from_string(temp_file.name)
            self.fail()
        except DataStoreException as dse:
            self.assertTrue(dse.message.startswith("You cannot read/write"), dse.message)

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


