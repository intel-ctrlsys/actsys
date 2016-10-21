#!/usr/bin/env python
"""Run all py.test tests under coverage in the folder tree."""
import coverage
import py.test

if __name__ == '__main__':
    cov = coverage.coverage(branch=True, config_file=True)
    cov.start()

    py.test.main()

    cov.stop()
    cov.save()
    cov.report(ignore_errors=True, show_missing=True)
    cov.html_report(directory='.html')
