#
# Copyright (c) 2017 Intel Inc. All rights reserved
#
import os
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import sqlalchemy
import unittest
import subprocess


HOST = "10.10.38.79"
PORT = "5432"
DB_NAME = "control_test_db"
USER = "ctrluser"
PASSWORD = "control"

# Database connection
DB_URL = sqlalchemy.engine.url.URL("postgresql", database=DB_NAME,
                                   username=USER, password=PASSWORD,
                                   host=HOST, port=PORT)

DATABASE_DIR_PATH = os.path.join("..", "database_schema")


class TestDBSchemaMigration(unittest.TestCase):
    def setUp(self):
        super(TestDBSchemaMigration, self).setUp()
        self.assertTrue(os.path.exists(DATABASE_DIR_PATH),
                        msg="Path '%s' does not exist.  "
                            "Cannot run test without files expected in '%s'" %
                            (DATABASE_DIR_PATH, DATABASE_DIR_PATH))
        # Connect to DB just to check connection only
        db_conn = create_engine(DB_URL).connect()
        self.assertIsNotNone(db_conn)
        db_conn.close()

        # Start from the base
        self._run_alembic("downgrade base")

    def tearDown(self):
        super(TestDBSchemaMigration, self).tearDown()
        # End at the base
        self._run_alembic("downgrade base")

    def _run_alembic(self, alembic_cmd):
        """Run Alembic CLI command with proper commandline options.
        :param alembic_cmd: A valid alembic command
        :return: Standard output
        """
        return subprocess.check_output(
            "alembic -c schema_migration.ini "
            "-x db_url=%s %s" % (DB_URL, alembic_cmd),
            shell=True,
            cwd=DATABASE_DIR_PATH)

    def test_db_schema_migration_script(self):
        """Test the 'setup_controldb.py script, and also the complete path of
        upgrade and downgrade of all schema revisions from base to head.
        """
        self.assertEqual("", self._run_alembic("current"))
        self.assertIn("Starting Alembic upgrade",
                      subprocess.check_output(
                          "python setup_controldb.py "
                          "--alembic-ini=schema_migration.ini",
                          shell=True,
                          cwd=DATABASE_DIR_PATH,
                          env={"PG_DB_URL": str(DB_URL)}))
        self.assertIn("(head)", self._run_alembic("current"))
        self.assertEqual("", self._run_alembic("downgrade base"))
        self.assertEqual("", self._run_alembic("current"))
        self.assertEqual("", self._run_alembic("upgrade head"))
        self.assertIn("(head)", self._run_alembic("current"))


if __name__ == "__main__":
    unittest.main()
