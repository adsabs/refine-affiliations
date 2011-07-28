# -*- encoding: utf-8 -*-

import sys
import unittest

if sys.hexversion < 0x02060000:
    print 'ERROR: Python version should be at least 2.6.'
    sys.exit(1)

from google.refine import refine

try:
    import ads_refine.create_refine_project as create
    import ads_refine.export_from_refine_project as export
except ImportError:
    import os
    sys.path.append(os.getcwd())
    import ads_refine.create_refine_project as create
    import ads_refine.export_from_refine_project as export

TEST_DATA = 'tests/test.affils.merged'

class TestRefineCreation(unittest.TestCase):

    def setUp(self):
        project_id = create.create_refine_project(TEST_DATA, 'Test project (can be safely removed).')
        # We need to reopen the project in order to force the refresh after
        # applying the JSON operations.
        server = refine.Refine(create.SERVER)
        self.project = server.open_project(project_id)

    def get_cell(self, row_number, column):
        row_number -= 1
        response = self.project.get_rows(start=row_number, limit=1)
        return response.rows[0][column]

    def test_columns(self):
        self.assertEqual(self.project.columns, ['Original', 'Without email', 'Emails', 'Bibcodes'])

    def test_row_number(self):
        response = self.project.get_rows()
        self.assertEqual(response.total, 18)

    def test_entity_conversion(self):
        self.assertEqual(self.get_cell(2, 'Without email'), 'Istituto Astronomico, Università "La Sapienza", via G.M. Lancisi 29, I-00161 Roma, Italy'.decode('utf-8'))
        self.assertEqual(self.get_cell(5, 'Without email'), 'Astronomical Institute, Czechoslovak Academy of Sciences, Ondřejov Observatory, and Astronomical Institute, Brno University.'.decode('utf-8'))

    def test_quotes(self):
        self.assertEqual(self.get_cell(3, 'Without email'), 'Laboratoire "Astrophysique, Atomes et Molecules", Departement Atomes et Molecules en Astrophysique, Unite associee au CNRS No. 812, Observatoire de Paris-Meudon, 92190 Meudon, France')
        self.assertEqual(self.get_cell(11, 'Without email'), "Institut d'Astrophysique de Paris 98bis, Bd Arago 75014 Paris, France")

    def test_emails(self):
        self.assertEqual(eval(self.get_cell(18, 'Emails')), [])
        self.assertEqual(eval(self.get_cell(10, 'Emails')), ["vittorio@astr1pi.difi.unipi.it"])
        self.assertEqual(eval(self.get_cell(9, 'Emails')), ["beersatmsupa.pa.msu.edukriessleratmsupa.pa.msu.edu", "tbirdatkula.phsx.ukans.edu"])
        # Email with a double quote.
        self.assertEqual(self.get_cell(4, 'Emails'), r'["yma@fyslab.hut.fi\""]')
        self.assertEqual(eval(self.get_cell(4, 'Emails')), ['yma@fyslab.hut.fi"'])

    def test_bibcodes(self):
        self.assertEqual(self.get_cell(11, 'Bibcodes'), '1997A&AS..121..407L,0')
        self.assertEqual(self.get_cell(17, 'Bibcodes'), '1981MitAG..52..127S,0 1981gjsa.proc..291S,0')

    def tearDown(self):
        self.project.delete()

class TestRefineExport(unittest.TestCase):

    def setUp(self):
        project_id = create.create_refine_project(TEST_DATA, 'Test project (can be safely removed).')
        # We need to reopen the project in order to force the refresh after
        # applying the JSON operations.
        server = refine.Refine(create.SERVER)
        self.project = server.open_project(project_id)
        rows = export.get_tsv_rows(project_id)
        self.affs = export.format_rows(rows)

    def test_number_of_affiliations(self):
        self.assertEqual(len(self.affs), 19)

    def test_absence_of_unicode(self):
        try:
            for aff in self.affs:
                aff.decode('ascii')
        except UnicodeDecodeError:
            raise

    def tearDown(self):
        self.project.delete()

if __name__ == '__main__':
    unittest.main()
