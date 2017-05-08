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

    datastore = DataStoreBuilder.get_datastore_from_string(os.environ.get("DATASTORE_LOCATION"))
    return_value = DataStoreCLI(datastore).parse_and_run()
    exit(return_value)

if __name__ == "__main__":
    main()
