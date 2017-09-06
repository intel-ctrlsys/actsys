from unittest import TestCase

from oobrestserver.GlobTools import GlobTools

class TestRegexTranslation(TestCase):

    def test_regexes(self):
        pairs = {
            '*': '[^/]*$',
            '**': '.*$',
            '(1000|1004)': '(1000|1004)$',
            '1000/*/*': '1000/[^/]*/[^/]*$',
            '1000/**': '1000/.*$',
            '*/**': '[^/]*/.*$',
            '100[1-4]': '100[1-4]$',
            '100[!1-4]': '100[^1-4]$',
        }
        for glob in pairs:
            regex = pairs[glob]
            result = GlobTools.regex_from_glob(glob)
            self.assertEqual(regex, result)
        

