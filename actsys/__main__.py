# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 <company or person>
#
"""
This is the main file, it is invoked when someone runs python like:
    python -m starter
"""

from .actsys import StartExample


def main():
    StartExample().run()

if __name__ == "__main__":
    main()
