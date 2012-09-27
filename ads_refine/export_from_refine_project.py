#!/usr/bin/python2.6

import os
import re
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

def extract_affiliations(project_id, modified_only=False):
    """
    Formats the raw output from Refine into an ADS-readable file.
    """
    p = refine.RefineProject(SERVER, project_id=project_id)

    # Check the columns.
    if p.columns != ['Original affiliation', 'New affiliation', 'Original emails', 'New emails', 'Bibcodes and positions']:
        raise Exception('ERROR: Columns are not as expected.')

    rows = p.export(export_format='tsv')
    # Skip the first row that contains the column names.
    rows.next()
    for row in rows:
        row = UNICODE_HANDLER.u2ent(row[:-1])
        original_aff, new_aff, original_emails, new_emails, bibcodes = row.split('\t')

        original = rebuild_affiliation(original_aff, original_emails)
        new = rebuild_affiliation(new_aff, new_emails)

        if modified_only and original == new:
            continue

        for bibcode in bibcodes.split(' '):
            bibcode, position = bibcode.split(',', 1)
            yield  '%s\t%s\t%s' % (bibcode, position, new)

def rebuild_affiliation(aff, emails):
    """
    Combines the affiliation and the emails.
    """
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

def latest_ast_affiliations_project_id():
    """
    Returns the project id of the latest astronomy affiliations project.
    """
    server = refine.Refine(SERVER)
    name_pattern = re.compile('affils.ast.\d{8}_\d{4}')

    latest_project = ('', None)
    for id, properties in server.list_projects().items():
        match = name_pattern.search(properties['name'])
        if match is not None:
            file_name = match.group()
            if file_name > latest_project[0]:
                latest_project = (file_name, id)

    return latest_project[1]

def main():
    t0 = time.time()

    usage = "usage: %prog [options] output_file"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--project-id", dest="project_id",
            help="export rows from project ID", metavar="ID")
    parser.add_option("-m", "--modified-only", dest="modified_only",
            help="exported modified rows only", action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose",
            help="verbose output", action="store_true")

    options, args = parser.parse_args()
    if not args or len(args) > 1:
        print 'Output file is required.'
        parser.print_usage()
        return
    else:
        output_file = args[0]
        if os.path.exists(output_file):
            os.remove(output_file)

    project_id = options.project_id if options.project_id else latest_ast_affiliations_project_id()

    print 'Exporting affiliations from project %d to file %s.' % (project_id, output_file) 

    fs = open(output_file, 'a')
    for index, affiliation in enumerate(extract_affiliations(project_id, options.modified_only)):
        fs.write(affiliation + '\n')
        if index % 50000 == 0:
            print 'Done %d.' % index
    fs.close()

    total_time = time.time() - t0
    print 'Done in %.2f seconds.' % total_time

if __name__ == '__main__':
    main()
