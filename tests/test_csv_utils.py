# -*- encoding: utf-8 -*-

import sys
import unittest

try:
    import ads_refine.csv_utils as csv_utils
except ImportError:
    import os
    sys.path.append(os.getcwd())
    import ads_refine.csv_utils as csv_utils

class TestCsvUtils(unittest.TestCase):

    def test_unescape(self):
        self.assertEqual(csv_utils.unescape_csv('No quotes',), 'No quotes')
        self.assertEqual(csv_utils.unescape_csv("'Single quotes'",), "'Single quotes'")
        self.assertEqual(csv_utils.unescape_csv("\"test \"\"a\"\" test\"",), 'test "a" test')
        self.assertEqual(csv_utils.unescape_csv("\"\"\"\"",), '"')

    def test_escape(self):
        self.assertEqual(csv_utils.escape_csv('No quotes'), 'No quotes',)
        self.assertEqual(csv_utils.escape_csv("'Single quotes'"), "'Single quotes'",)
        self.assertEqual(csv_utils.escape_csv('test "a" test'), "\"test \"\"a\"\" test\"",)
        self.assertEqual(csv_utils.escape_csv('"'), "\"\"\"\"",)

if __name__ == '__main__':
    unittest.main()
