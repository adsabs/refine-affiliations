#!/usr/bin/python2.6

from optparse import OptionParser
import sys
from google.refine import refine
import os

from clean_ads_affiliations import clean_ads_affs

SERVER = 'http://adsx.cfa.harvard.edu:3333'

def create_refine_project(path, name):

    r  = refine.Refine(SERVER)

    x = r.new_project(project_file=path,
            project_name='%s (%s)' % (name, os.path.basename(path).replace('.reversed', '.merged')), 
            split_into_columns=False,
            separator='',
            ignore_initial_non_blank_lines=0,
            header_lines=0,
            skip_initial_data_rows=0,
            limit=0,
            guess_value_type=False,
            ignore_quotes=False)

    print "-- Project has been created. Now applying some few operations."

    x.apply_operations('create-project-operations.json')

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_file",
            help="create Refine project from FILE", metavar="FILE")
    parser.add_option("-t", "--title", dest="title",
            help="create Refine project with TITLE", metavar="TITLE")

    options, args = parser.parse_args()
    input_file = os.path.abspath(options.input_file)
    title = options.title
    print 'Create a file that we can upload to Refine.'
    new_input_file = clean_ads_affs(input_file)
    print 'Upload to Refine.'
    create_refine_project(new_input_file, title)
    print 'Done with success.'

if __name__ == '__main__':
    main()
