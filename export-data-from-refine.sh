#!/bin/bash -xe

AFFILIATION_HOME=`pwd`

source $AFFILIATION_HOME/python/bin/activate
output_file=$AFFILIATION_HOME/extracted_affiliations/output/affils.ast.`date +'%Y%m%d_%H%M%S'`.output

# This automatically selects the latest astronomy affiliations project from Google Refine.
python scripts/from_refine --modified-only $output_file

deactivate