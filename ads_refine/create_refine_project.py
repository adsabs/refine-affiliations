#!/usr/bin/python2.6

import os
import sys
from optparse import OptionParser
from google.refine import refine

from clean_ads_affiliations import clean_ads_affs

assert sys.hexversion >= 0x02060000

SERVER = 'http://adsx.cfa.harvard.edu:3333'

def create_refine_project(path, name, pretend=False, verbose=0):
    input_file = os.path.abspath(path)
    msg('Create a file that we can upload to Refine.', verbose)
    new_input_file = clean_ads_affs(input_file, verbose)
    msg('Upload to Refine.', verbose)
 
    if not pretend:
        r  = refine.Refine(SERVER)
        project = r.new_project(project_file=new_input_file,
                project_name='Astronomy affiliations (%s)' % (os.path.basename(path).replace('.reversed', '.merged')),
                split_into_columns=True,
                separator='\t',
                ignore_initial_non_blank_lines=0,
                header_lines=1,
                skip_initial_data_rows=0,
                limit=0,
                guess_value_type=False,
                ignore_quotes=False)

        msg('Done with success.', verbose)

        return project.project_id

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_file",
            help="create Refine project from FILE", metavar="FILE")
    parser.add_option("-t", "--title", dest="title",
            help="create Refine project with TITLE", metavar="TITLE")
    parser.add_option("--pretend", dest="pretend", action="store_true", default=False,
            help="do not upload affiliations")
    options, _ = parser.parse_args()
    
    create_refine_project(options.input_file, options.title, options.pretend, 1)

def msg(message, verbose):
    if verbose:
        print message

if __name__ == '__main__':
    main()
