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

def format_affiliations(project_id, modified_only=False):
    """
    Formats the raw output from Refine into an ADS-readable file.
    """
    p = refine.RefineProject(SERVER, project_id=project_id)

    # Check the columns.
    if p.columns != ['Original affiliation', 'Original emails', 'New emails', 'Original emails', 'Bibcodes and positions']:
        print p.columns
        ['Original affiliation', 'New affiliation', 'Original emails', 'New emails', 'Bibcodes and positions']
        print ['Original affiliation', 'New affiliation', 'New emails', 'Original emails', 'Bibcodes and positions']
        raise Exception('ERROR: Columns are not as expected.')

    rows = p.export(export_format='tsv')

    affiliations = []

    # Skip the first row that contains the column names.
    _ = rows.next()
    for row in rows:
        row = UNICODE_HANDLER.u2ent(row[:-1].decode('utf-8'))
        original_aff, new_aff, new_emails, original_emails, bibcodes = \
                row.split('\t')

        original = rebuild_affiliation(original_aff, original_emails)
        new = rebuild_affiliation(new_aff, new_emails)

        if modified_only and original == new:
            continue

        for bibcode in bibcodes.split(' '):
            bibcode, position = bibcode.split(',', 1)
            affiliations.append('%s\t%s\t%s' % (bibcode, position, new))

    return sorted(affiliations)

def rebuild_affiliation(aff, emails):
    aff = unescape_csv(aff)
    emails = unescape_csv(emails)
    emails = create_email_string(emails)

    if aff and emails:
        return '%s %s' % (aff, emails)
    elif aff:
        return aff
    elif emails:
        return emails
    else:
        return ''

def create_email_string(email_field):
    if not email_field:
        return ''
    elif email_field == '[]':
        return ''
    else:
        emails = unescape_csv(email_field)
        try:
            emails = eval(emails)
        except SyntaxError:
            raise Exception("ERROR: Email field is not well formatted: '%s'." % 
                    emails)

        return '<EMAIL>%s</EMAIL>' % '</EMAIL> <EMAIL>'.join(emails)

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
    parser.add_option("-m", "--modified-only", dest="modified_only",
            help="exported modified rows only", action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose",
            help="verbose output", action="store_true")

    options, _ = parser.parse_args()

    affiliations = format_affiliations(options.project_id,
            options.modified_only)
    write_affiliations_to_file(options.output_file, affiliations)
    total_time = time.time() - t0
    print 'Done in %.2f seconds.' % total_time

if __name__ == '__main__':
    main()
