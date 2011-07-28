import unittest

try:
    import ads-refine.create_refine_project as create
except ImportError:
    import sys
    sys.path.append(os.getcwd())
    import ads-refine.create_refine_project as create

TEST_DATA = 'ads-refine/test.affils.merged'

class TestRefineCreation(unittest.TestCase):

    def setUp(self):
        self.project = create.create_refine_project(TEST_DATA, 'Test project (can be safely removed).')

    def test_columns(self):
        self.assertEqual(self.project.columns, ['Original', 'Without email', 'Emails', 'Bibcodes'])

    def tearDown(self):
        self.project.delete()

if __name__ == '__main__' 
