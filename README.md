# actsys
Actsys is a unified tool that allows user to execute administrative and operational commands on clusters and supercomputers. Actsys aims to hide complexities of supercomputers and targets at exascale. 

[![Documentation status](https://readthedocs.org/projects/actsys/badge/?version=latest)](http://actsys.readthedocs.io/en/latest/) [![Build Status](https://travis-ci.org/intel-ctrlsys/actsys.svg?branch=master)](https://travis-ci.org/intel-ctrlsys/actsys) [![codecov](https://codecov.io/gh/intel-ctrlsys/actsys/branch/master/graph/badge.svg)](https://codecov.io/gh/intel-ctrlsys/actsys)

Documentation: http://actsys.readthedocs.io/en/latest/

# Project Details

## Structure

This project follows the structure suggested in [Jan-Philip Gehrcke's Blog](https://gehrcke.de/2014/02/distributing-a-python-command-line-application/).
This project has two main parts, namely ctrl and datastore (The two main directories). Ctrl handles all the command business logic, while datastore manages state data of the cluster, such as configuration, journal logging and logical group. In order for ctrl to work, one needs to install datastore first. Please refer to [ctrl readme](https://github.com/intel-ctrlsys/actsys/blob/master/ctrl/README.md) and [datastore readme](https://github.com/intel-ctrlsys/actsys/blob/master/datastore/README.md) for more details about ctrl and datastore.

## Versioning

This project uses [Semver](http://semver.org/) as its versioning scheme. Versions are marked with tag and show up in the [releases section of github](https://github.com/intel-ctrlsys/actsys/releases).

To learn how to tag a new version, see the [git tag tutorial](https://git-scm.com/book/en/v2/Git-Basics-Tagging). If you mess up, you can always [delete a tag](https://stackoverflow.com/questions/5480258/how-to-delete-a-git-remote-tag).

## Tests

Ctrl and datastore projects include unit tests in their source folders (ctrl/control, datastore/datastore). In ctrl, each component has individual unit tests in their folder. In datastore, all the tests are in the tests folder. To run the tests, go to ctrl or datastore directory and then execute `python -m pytest .`.

The tests are ran automatically when they are submitted to github via [travici.org](https://travis-ci.org/intel-ctrlsys/actsys). Your tests must work here to be considered passing, it doesn't matter if they run on your local machine, if they fail on TravisCI, then they will not be accepted into matser.

Coverage is also determined by TravisCI and reported to [CodeCov](https://codecov.io/gh/intel-ctrlsys/actsys).

## Documentation

Documentation is inline and deployed with [Read the Docs](http://actsys.readthedocs.io/en/latest/). When editing code, please include documentation for your changes. Add any new files to the `mkdocs.yml` file. The documentation is automatically built and installed.

The documentation is found here: http://actsys.readthedocs.io/en/latest/

You can test the docs locally by installing [mkdocs](http://www.mkdocs.org/) and running `mkdocs serve` in the root directory of the project source. This will launch a server locally that you can use to view what the docs will look like when deployed. The pages update automatically when changes are made.

You can add a page to the documentation by editing the *mkdocs.yml* file in the source repo. See [Adding Pages](http://www.mkdocs.org/#adding-pages).
