#!/bin/bash

files=`find . -name '*.py' -print | grep -v -e __init__.py -e run-coverage.py | grep -v -E 'test_.+\.py'`
pylint $files | tee .pylint.out
