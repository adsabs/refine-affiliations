import sys
import time
import unittest

if sys.hexversion < 0x02060000:
    print 'ERROR: Python version should be at least 2.6.'
    sys.exit(1)

from google.refine import refine

try:
    import ads_refine.create_refine_project as create
except ImportError:
    import os
    import sys
    sys.path.append(os.getcwd())
    import ads_refine.create_refine_project as create

TEST_DATA = 'tests/test.affils.merged'

class TestRefineCreation(unittest.TestCase):

    def setUp(self):
        project_id = create.create_refine_project(TEST_DATA, 'Test project (can be safely removed).')
        # We need to reopen the project in order to force the refresh after applying the JSON operations.
        server = refine.Refine(create.SERVER)
        self.project = server.open_project(project_id)

    def test_columns(self):
        self.assertEqual(self.project.columns, ['Original', 'Without email', 'Emails', 'Bibcodes'])

    def test_row_number(self):
        response = self.project.get_rows()
        self.assertEqual(response.total, 17)

    def tearDown(self):
        self.project.delete()

if __name__ == '__main__':
    unittest.main()
