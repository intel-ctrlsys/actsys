# -*- coding: utf-8 -*-
"""
Contains the GlobTools class, which provides methods for working with glob
expressions in a similar way to regexes.
"""

import re


class GlobTools():
    """
    Provides static methods supporting matching and filtering with glob
    expressions
    """

    @staticmethod
    def filter(strings, glob):
        return [elt for elt in strings if GlobTools.match(elt, glob)]

    @staticmethod
    def match(string, glob):
        return bool(re.match(GlobTools.regex_from_glob(glob), string))

    @staticmethod
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
