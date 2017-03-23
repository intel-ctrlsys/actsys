# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#

"""control.__main__: executed when bootstrap directory is called as script."""
import os
import logging
from sys import exit
from . import DataStoreBuilder, DataStoreCLI, get_logger

def main(args=None):
    """
    The main entry point
    :param args:
    :return:
    """

    datastore = None
    dsb = DataStoreBuilder()
    dsb.set_print_to_screen(True, logging.INFO)
    dsb.add_postgres_db(os.environ.get("PG_DB_URL"), logging.INFO)
    try:
        get_logger().critical("foo")
        datastore = dsb.build()
        # datastore = DataStoreBuilder.get_datastore_from_env_vars(postgres_env_var="PG_DB_URL")
    except Exception as e:
        print(e)
        exit(1)

    return_value = DataStoreCLI(datastore).parse_and_run()
    exit(return_value)

if __name__ == "__main__":
    main()
