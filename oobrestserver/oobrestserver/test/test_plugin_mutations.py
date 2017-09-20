
from unittest import TestCase

from oobrestserver.Plugin import Plugin

class TestPluginMutations(TestCase):

    def test_search_resources(self):

        sample_data = {
            "A": {
                "B": {
                    "C": "/a/b/c",
                    "F": "/a/b/f"
                },
                "D": {
                    "F": "/a/d/f",
                    "E": "/a/d/e",
                    "G": {
                        "H": {
                            "I": "/a/d/g/h/i",
                            "F": "/a/d/g/h/f"
                        }
                    }
                }
            }
        }

        tests = [
            ([], 1),
            (["A"], 1),
            (["A", "B"], 1),
            (["A", "B", "C"], 1),
            (["A", "B", "F"], 1),
            (["A", "D", "F"], 1),
            (["A", "D", "E"], 1),
            (["A", "D", "G"], 1),
            (["*"], 1),
            (["A", "*"], 2),
            (["A", "B", "*"], 2),
            (["A", "D", "*"], 3),
            (["A", "*", "*"], 5),
            (["*", "*", "*"], 5),
            (["A", "*", "*", "*"], 1),
            (["A", "*", "*", "*", "*"], 2),
            # (["**", "F"], 3)
        ]

        for test in tests:
            print(test)
            self.assertEqual(len(Plugin.search_resources(sample_data, test[0])), test[1])
