# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
A helper module to help a user configurate DataStore and create an instance to their liking.
"""
import os
from .datastore import DataStore, DataStoreException, get_logger, add_stream_logger
from .filestore import FileStore
from .postgresstore import PostgresStore
from .multistore import MultiStore


class DataStoreBuilder(object):
    """
    DataStoreBuilder: The interface to build a DataStore that will work for your needs.
    """

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
        self.dbs.append(FileStore(location, log_level))
        return self

    def add_postgres_db(self, connection_uri, log_level=None):
        """

        :param connection_uri:
        :param log_level: The level in which you want logging done at.
        :return:
        """
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
    def get_datastore_from_string(datastore_location, screen_log_level=None):
        """
        Creates an instance of the datastore that works with the string passed in. Sets up the printing to screen
        with the log level specificed (or a default one).
        :param datastore_location: Either a file location (like /etc/datastore_db) or
            a postgres uri (See https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING )
        :param screen_log_level:
        :return:
        :raise: DataStoreException, if the string doesn't connect to anything.
        """
        if not isinstance(datastore_location, str):
            raise ValueError("datastore parameter must be a string")

        if screen_log_level is None:
            screen_log_level = DataStore.LOG_LEVEL
        add_stream_logger(get_logger(), screen_log_level)

        if datastore_location.startswith("postgres://"):
            return PostgresStore(datastore_location)
        elif os.path.isfile(datastore_location):
            return FileStore(datastore_location)

        try:
            # Perhaps this is a PostgresStore of a different location
            return PostgresStore(datastore_location)
        except:
            # Something went wrong connecting, assume it was a bad connection string and continue trying.
            pass
        try:
            # Maybe this is a valid location that doesn't already have a file.
            return FileStore(datastore_location)
        except IOError:
            raise DataStoreException("You cannot read/write the configuration database at {}. Do you have sufficient"
                                     " permissions?".format(datastore_location))
        except:
            pass

        # Could not find any suitable postgreSQL or file location. Default to FileStore default location.
        raise DataStoreException("The string '{}' could not be used to connection to either PostgresSQL or a"
                                 " file".format(datastore_location))

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
