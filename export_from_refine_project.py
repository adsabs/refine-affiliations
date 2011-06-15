#!/usr/bin/python2.6

from optparse import OptionParser
import sys
import simplejson
from google.refine import refine

sys.path.append('/proj/ads/soft/python/lib/site-packages')
import ads.Unicode as Unicode

UNICODE_HANDLER = Unicode.UnicodeHandler()

SERVER = 'http://adsx.cfa.harvard.edu:3333'

class RefineExportException(Exception):
    pass

def export_project_in_json(project_id):
    p = refine.RefineProject(SERVER, project_id=project_id)
    json = p.export(export_format='json').read()
    return json

def unpack_exported_json_file(json, changed_only=False):
    """
    Reads the raw JSON refine project and returns a list of affiliations that
    can be put back in ADS.
    """
    json = simplejson.loads(json)
    rows = json['rows']

    output_affs = []

    for row in rows:
        aff_original = row['Original']
        aff = row['Without email']
        emails = row['Emails']
        bibcodes = row['Bibcodes']

        if emails:
            emails = eval(emails)
            emails = '<EMAIL>%s</EMAIL>' % '</EMAIL><EMAIL>'.join(emails)
        
        if aff and emails:
            aff = aff + emails
        elif emails:
            aff = emails
        elif aff is None:
            aff = ''

        if not changed_only or aff != original:
            for bibcode in bibcodes.split(' '):
                output_affs.append('%s\t%s' % (bibcode, aff))

    return output_affs

def write_affiliations_to_file(path):
    fs = codecs.open(path, mode='w', encoding='UTF-8')


def main():
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="output_file",
            help="export Refine project to FILE", metavar="FILE")
    parser.add_option("-p", "--project-id", dest="project_id",
            help="export rows from project ID", metavar="ID")
    parser.add_option("-", "--verbose", dest="verbose",
            help="export rows from project ID", metavar="ID")

    options, args = parser.parse_args()

    json = export_project_in_json(options.project_id)

if __name__ == '__main__':
    main()
