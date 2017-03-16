# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#

"""control.__main__: executed when bootstrap directory is called as script."""
import os
import logging
from . import DataStoreBuilder, DataStoreCLI
from sys import exit

def main(args=None):
    """
    The main entry point
    :param args:
    :return:
    """

    datastore = None
    dsb = DataStoreBuilder()
    dsb.add_postgres_db(os.environ.get("PG_DB_URL"), logging.INFO)
    dsb.set_print_to_screen(True, logging.DEBUG)
    try:
        datastore = dsb.build()
        # datastore = DataStoreBuilder.get_datastore_from_env_vars(postgres_env_var="PG_DB_URL")
    except Exception as e:
        print(e)
        exit(1)

    return_value = DataStoreCLI(datastore).parse_and_run()
    exit(return_value)

if __name__ == "__main__":
    main()
