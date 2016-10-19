#!/usr/bin/env python
"""
Run the pylint tool on all production code.
"""
import os.path
from pylint.lint import Run


class FolderWalker(object):
    """Walk a tree and get all .py files with exceptions."""
    def __init__(self):
        pass

    @classmethod
    def get_files_for_pylint(cls, folder):
        """Primary interface to get file path list."""
        file_list = []
        os.path.walk(folder, cls._visited_method, file_list)
        return file_list

    @classmethod
    def _visited_method(cls, file_list, directory, names):
        """Called by os.path.walk()."""
        exceptions = [
            '__init__.py',
            'run-coverage.py',
            'run-pylint.py'
        ]
        if '.git' in directory:
            return
        for filename in names:
            if filename.endswith('.py') and \
                    not filename.startswith('test_') and \
                    filename not in exceptions:
                file_list.append(os.path.join(directory, filename))


if __name__ == '__main__':
    files = FolderWalker.get_files_for_pylint('.')
    Run(files)
