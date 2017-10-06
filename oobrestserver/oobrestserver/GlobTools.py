# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Provides methods supporting matching and filtering with glob expressions
by translation to regexes.
"""

import re


def glob_filter(strings, glob):
    return [elt for elt in strings if glob_match(elt, glob)]

def glob_match(string, glob):
    return bool(re.match(regex_from_glob(glob), string))

def regex_from_glob(pattern):
    """FSM to convert globstar patterns to Python regexes"""

    state = 'start'
    result = ''
    bracket_set = ''
    bracket_negate = False

    for symbol in pattern:
        if state == '*':
            if symbol == '*':
                result += '.*'
                state = 'start'
            else:
                result += '[^/]*' + symbol
                state = 'start'
        elif state == '[':
            if symbol == '!':
                bracket_negate = True
            elif symbol == ']':
                if bracket_negate:
                    result += '[^' + bracket_set + ']'
                else:
                    result += '[' + bracket_set + ']'
                state = 'start'
            else:
                bracket_set += symbol
        else:
            if symbol == '*':
                state = '*'
            elif symbol == '?':
                result += '.'
            elif symbol == '[':
                bracket_negate = False
                state = '['
            else:
                result += symbol
    if state == '*':
        result += '[^/]*'
    elif state == '[':
        message = 'Invalid glob expression: open bracket not closed'
        raise ValueError(message)
    result += '$'
    return result
