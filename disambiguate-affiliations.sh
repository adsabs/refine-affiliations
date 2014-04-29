#!/bin/bash -xe

export PYTHONPATH=.:$PYTHONPATH

AFFILIATION_HOME=`pwd`

source $AFFILIATION_HOME/python/bin/activate


# This runs the disambiguation with the latest file extracted.
python $AFFILIATION_HOME/ads_refine/disambiguate.py -e $AFFILIATION_HOME/extracted_affiliations/input/`ls -t1 $AFFILIATION_HOME/extracted_affiliations/input/ | head -n1` "Astronomy affiliations disambiguation"

deactivate
