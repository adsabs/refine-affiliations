#!/usr/bin/python2.6

import sys
import time
from optparse import OptionParser

assert sys.hexversion >= 0x02060000

from google.refine import refine

from csv_utils import unescape_csv

try:
    import ads.Unicode as Unicode
except ImportError:
    sys.path.append('/proj/ads/soft/python/lib/site-packages')
    import ads.Unicode as Unicode

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

        if emails and emails != '[]':
            try:
                emails = eval(unescape_csv(emails))
                emails = '<EMAIL>%s</EMAIL>' % '</EMAIL> <EMAIL>'.join(emails)
                if new:
                    new = '%s %s' % (new, emails)
                else:
                    new = emails
            except SyntaxError:
                raise Exception('ERROR: Email field is not well formatted:' +
                        unescape_csv(emails))

        bibcodes = bibcodes.split(' ')
        for bibcode in bibcodes:
            bibcode, position = bibcode.split(',')
            affiliations.append('%s\t%s\t%s' % (bibcode, position, new))

    return sorted(affiliations)

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
