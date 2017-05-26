# python-starter
A starting spot for python projects. Embracing open source elements.

[![Documentation status](https://readthedocs.org/projects/actsys/badge/?version=latest)](http://actsys.readthedocs.io/en/latest/) [![Build Status](https://travis-ci.org/intel-ctrlsys/actsys.svg?branch=master)](https://travis-ci.org/intel-ctrlsys/actsys) [![codecov](https://codecov.io/gh/intel-ctrlsys/actsys/branch/master/graph/badge.svg)](https://codecov.io/gh/intel-ctrlsys/actsys)

Documentation: http://actsys.readthedocs.io/en/latest/

# Project Details

## Structure

This project follows the structure suggested in [Jan-Philip Gehrcke's Blog](https://gehrcke.de/2014/02/distributing-a-python-command-line-application/).

## Versioning

This project uses [Semver](http://semver.org/) as its versioning scheme.

## Tests

Basic acceptance tests are in the tests folder. You can run these tests by running `python setup.py test`. The unit tests are in line with the code. You can run all the tests with `python -m pytest .`.

The tests are ran automatically when they are submitted to github via [travici.org](https://travis-ci.org/intel-ctrlsys/actsys). Your tests must work here to be considered passing, it doesn't matter if they run on your local machine, if they fail on TravisCI, then they will not be accepted into matser.

Coverage is also determined by TravisCI and reported to [CodeCov](https://codecov.io/gh/intel-ctrlsys/actsys).

## Documentation

Documentation is inline (like unit tests) and deployed with [Read the Docs](http://actsys.readthedocs.io/en/latest/). When editing code, please include documentation for your changes. Add any new files to the `mkdocs.yml` file. The documentation is automatically built and installed.

The documentation is found here: http://actsys.readthedocs.io/en/latest/

You can test the docs locally by installing [mkdocs](http://www.mkdocs.org/) and running `mkdocs serve` in the root directory of the project source. This will launch a server locally that you can use to view what the docs will look like when deployed. The pages update automatically when changes are made.

You can add a page to the documentation by editing the *mkdocs.yml* file in the source repo. See [Adding Pages](http://www.mkdocs.org/#adding-pages).
