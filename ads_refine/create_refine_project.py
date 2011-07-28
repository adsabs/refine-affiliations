#!/usr/bin/python2.6

from optparse import OptionParser
from google.refine import refine
import os

from clean_ads_affiliations import clean_ads_affs

SERVER = 'http://adsx.cfa.harvard.edu:3333'

def create_refine_project(path, name, verbose=0):
    input_file = os.path.abspath(path)
    msg('Create a file that we can upload to Refine.', verbose)
    new_input_file = clean_ads_affs(input_file)
    msg('Upload to Refine.', verbose)

    r  = refine.Refine(SERVER)
    project = r.new_project(project_file=new_input_file,
            project_name='%s (%s)' % (name, os.path.basename(path).replace('.reversed', '.merged')),
            split_into_columns=True,
            separator='\t',
            ignore_initial_non_blank_lines=0,
            header_lines=0,
            skip_initial_data_rows=0,
            limit=0,
            guess_value_type=False,
            ignore_quotes=False)

    msg("-- Project has been created. Now applying a few operations.", verbose)

    project.apply_operations('ads_refine/create-project-operations.json')

    msg('Done with success.', verbose)

    return project.project_id

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_file",
            help="create Refine project from FILE", metavar="FILE")
    parser.add_option("-t", "--title", dest="title",
            help="create Refine project with TITLE", metavar="TITLE")
    options, _ = parser.parse_args()
    
    create_refine_project(options.input_file, options.title, 1)

def msg(message, verbose):
    if verbose:
        print msg

if __name__ == '__main__':
    main()
