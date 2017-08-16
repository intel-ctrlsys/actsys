from unittest import TestCase

from ..ParallelDispatcher import ParallelDispatcher

class TestRegexTranslation(TestCase):

    def test_regexes(self):
        pairs = {
            '*': '[^/]*$',
            '**': '.*$',
            '(1000|1004)': '(1000|1004)$',
            '1000/*/*': '1000/[^/]*/[^/]*$',
            '1000/**': '1000/.*$',
            '*/**': '[^/]*/.*$'
        }
        for glob in pairs:
            regex = pairs[glob]
            result = ParallelDispatcher.regex_from_glob(glob)
            self.assertEqual(regex, result)
        

