#!/usr/bin/python2.6

import time
from optparse import OptionParser
from google.refine import refine

import ads.Unicode as Unicode
from csv_utils import unescape_csv

UNICODE_HANDLER = Unicode.UnicodeHandler()

SERVER = 'http://adsx.cfa.harvard.edu:3333'

def get_tsv_rows(project_id):
    p = refine.RefineProject(SERVER, project_id=project_id)
    return p.export(export_format='tsv')

def format_rows(rows):
    """
    Formats the raw output from Refine into an ADS-readable file.
    """
    affiliations = []

    _ = rows.next()
    for row in rows:
        row = UNICODE_HANDLER.u2ent(row[:-1].decode('utf-8'))
        original, new, emails, bibcodes = row.split('\t')

        new = unescape_csv(new)

        try:
            emails = eval(unescape_csv(emails))
            if emails:
                emails = '<EMAIL>%s</EMAIL>' % '</EMAIL><EMAIL>'.join(emails)
                new += emails
        except SyntaxError:
            print 'Problem with row:\n' + row

        bibcodes = bibcodes.split(' ')
        for bibcode in bibcodes:
            affiliations.append('%s\t%s' % (bibcode, new))

    return affiliations

def write_affiliations_to_file(path, affs):
    fs = open(path, 'w')
    fs.write('\n'.join(affs))
    fs.close()

def main():
    t0 = time.time()

    parser = OptionParser()
    parser.add_option("-o", "--output", dest="output_file",
            help="export Refine project to FILE", metavar="FILE")
    parser.add_option("-p", "--project-id", dest="project_id",
            help="export rows from project ID", metavar="ID")
    parser.add_option("-v", "--verbose", dest="verbose",
            help="export rows from project ID", metavar="ID")

    options, _ = parser.parse_args()

    rows = get_tsv_rows(options.project_id)
    print 'The project %s has been exported.' % options.project_id
    print 'Formatting the output.'
    affiliations = format_rows(rows)
    print 'Writing to the output file: %s.' % options.output_file
    write_affiliations_to_file(options.output_file, affiliations)
    total_time = time.time() - t0
    print 'Done in %.2f seconds.' % total_time

if __name__ == '__main__':
    main()
