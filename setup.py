# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Setup Module
"""
from setuptools import setup, find_packages

description = "A control component for exascale clusters"
author = "Intel Corporation"
license = "Apache"

setup(name='ctrl',
      version='0.1.0',
      description=description,
      author=author,
      license=license,
      packages=find_packages(),
      scripts=['ctrl'],
      install_requires=['psycopg2', 'python-dateutil'],
      test_suite='tests',
      tests_require=['coverage',
                     'pytest',
                     'pylint',
                     'mock'])
