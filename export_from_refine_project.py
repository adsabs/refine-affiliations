#!/usr/bin/python2.6

from optparse import OptionParser
import sys
import json
from google.refine import refine
import urllib

sys.path.append('/proj/ads/soft/python/lib/site-packages')
import ads.Unicode as Unicode
from csv_utils import unescape_csv

UNICODE_HANDLER = Unicode.UnicodeHandler()

SERVER = 'http://adsx.cfa.harvard.edu:3333'

class RefineExportException(Exception):
    pass

def get_tsv_rows(project_id):
    p = refine.RefineProject(SERVER, project_id=project_id)
    return p.export(export_format='tsv')

def format_rows(rows):
    """
    Formats the raw output from Refine into an ADS-readable file.
    """
    affiliations = []

    title = rows.next()
    for row in rows:
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
            affiliations.append(bibcode + '\t' + new)

    return affiliations

def write_affiliations_to_file(path, affs):
    fs = open(path, 'w')
    fs.writelines(affs)
    fs.close()

def main():
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="output_file",
            help="export Refine project to FILE", metavar="FILE")
    parser.add_option("-p", "--project-id", dest="project_id",
            help="export rows from project ID", metavar="ID")
    parser.add_option("-v", "--verbose", dest="verbose",
            help="export rows from project ID", metavar="ID")

    options, args = parser.parse_args()

    rows = get_tsv_rows(options.project_id)
    print 'The project %s has been exported.' % options.project_id
    print 'Formatting the output.'
    affiliations = format_rows(rows)
    print 'Writing to the output file: %s.' % options.output_file
    write_affiliations_to_file(options.output_file, affiliations)
    print 'Done.'

if __name__ == '__main__':
    main()
