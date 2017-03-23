# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
import os
from .datastore import DataStore, DataStoreException, get_logger, add_stream_logger
from .filestore import FileStore
from .postgresstore import PostgresStore
from .multistore import MultiStore


class DataStoreBuilder(object):
    """
    DataStoreBuilder: The interface to build a DataStore that will work for your needs.
    """
    FILESTORE_DEFUALT_LOCATION = os.path.join(os.getenv('HOME'), "datastore.json")
    FILESTORE_DEFAULT_CONFIG = """{
  "configuration_variables": {
  },
  "device": [
  ],
  "profile": [
  ]
}"""

    def __init__(self):
        self.dbs = list()
        self.print_to_screen = False
        self.screen_log_level = DataStore.LOG_LEVEL

    def add_file_db(self, location, log_level=None):
        """
        Creates a filestore with the location you have specified. If no location is given, creates it
        in ~/datastore.json.
        :param location:
        :param log_level: The level in which you want logging done at.
        :return:
        """
        if log_level is None:
            log_level = DataStore.LOG_LEVEL

        if location is None:
            location = self.FILESTORE_DEFUALT_LOCATION
            if not os.path.isfile(location):
                config_file = open(location, 'w')
                config_file.write(self.FILESTORE_DEFAULT_CONFIG)
                config_file.close()

        self.dbs.append(FileStore(location, log_level))
        return self

    def add_postgres_db(self, connection_uri, log_level=None):
        """

        :param connection_uri:
        :param log_level: The level in which you want logging done at.
        :return:
        """
        if log_level is None:
            log_level = DataStore.LOG_LEVEL
        self.dbs.append(PostgresStore(connection_uri, log_level))
        return self

    def set_print_to_screen(self, print_to_screen=True, log_level=None):
        """

        :param print_to_screen: If this should happen or not.
        :param log_level: The level in which you want logging done at.
        :return:
        """
        if log_level is None:
            log_level = DataStore.LOG_LEVEL

        self.print_to_screen = print_to_screen
        self.screen_log_level = log_level
        return self

    def set_default_log_level(self, log_level):
        """
        Set the default log level for loggers/databases created. This will NOT affect already created databases!
        :param log_level: The level in which you want logging done at.
        :return:
        """
        DataStore.LOG_LEVEL = log_level
        return self

    def build(self):
        """

        :return:
        """
        if self.print_to_screen:
            add_stream_logger(get_logger(), self.screen_log_level)

        if len(self.dbs) > 1:
            return MultiStore(self.dbs)
        elif len(self.dbs) == 1:
            return self.dbs[0]
        else:
            raise DataStoreException("Cannot create a DataStore. No databases were selected (i.e file, postgresql).")

    @staticmethod
    def get_datastore_from_env_vars(print_to_screen=False, filestore_env_var="datastore_file_location",
                                    postgres_env_var="datastore_postgres_uri"):
        """
        Build A datastore based on the passed in ENV variables. This has less control, but its simple.
        :param print_to_screen:
        :param filestore_env_var:
        :param postgres_env_var:
        :return:
        """
        builder = DataStoreBuilder()
        builder.set_print_to_screen(print_to_screen)
        if os.environ.get(filestore_env_var, None) is not None:
            builder.add_file_db(os.environ.get(filestore_env_var))
        if os.environ.get(postgres_env_var, None) is not None:
            builder.add_postgres_db(os.environ.get(postgres_env_var))

        if len(builder.dbs) == 0:
            raise DataStoreException("Please specify a database. This can be done via the "
                                     "ENV variables: {} and {}".format(filestore_env_var, postgres_env_var))

        return builder.build()
