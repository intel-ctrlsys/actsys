# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
from .datastore import DataStore
from .filestore import FileStore
from .postgresstore import PostgresStore
from .multistore import MultiStore


class DataStoreBuilder(object):
    """
    DataStoreBuilder: The interface to build a datastore that will work for your needs.
    """
    def __init__(self):
        self.dbs = list()
        self.print_to_screen = False
        self.log_level = None

    def add_file_db(self, location):
        """

        :param location:
        :return:
        """
        self.dbs.append(FileStore(self.print_to_screen, location))
        return self

    def add_postgres_db(self, connection_uri):
        """

        :param connection_uri:
        :return:
        """
        self.dbs.append(PostgresStore(self.print_to_screen, connection_uri))
        return self

    def set_print_to_screen(self, print_to_screen=True):
        """

        :param print_to_screen:
        :return:
        """
        for db in self.dbs:
            db.print_to_screen = print_to_screen
        self.print_to_screen = print_to_screen
        return self

    def set_log_level(self, log_level):
        """

        :param log_level:
        :return:
        """
        for db in self.dbs:
            db.log_level = log_level
        self.log_level = log_level
        DataStore.LOG_LEVEL = log_level
        return self

    def build(self):
        """

        :return:
        """
        if len(self.dbs) > 1:
            return MultiStore(self.print_to_screen, self.dbs)
        else:
            return self.dbs[0]


