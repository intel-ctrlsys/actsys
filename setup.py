# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Setup Module
"""
from setuptools import setup, find_packages

description = "A datastore for exascle clusters"
author = "Intel Corporation"
license = "Apache"

setup(name='datastore',
      version='0.1.0',
      description=description,
      author=author,
      license=license,
      packages=find_packages(),
      entry_points={
          'console_scripts': ['datastore = datastore.__main__:main']
      },
      install_requires=['psycopg2', 'python-dateutil'],
      test_suite='tests',
      tests_require=['coverage',
                     'pytest',
                     'pylint',
                     'mock'])
