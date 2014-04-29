#!/bin/bash -xe

AFFILIATION_HOME=`pwd`

source $AFFILIATION_HOME/python/bin/activate

latest_affiliations=$AFFILIATION_HOME/extracted_affiliations/input/`ls -t1 $AFFILIATION_HOME/extracted_affiliations/input | head -n1`

python to_refine -i $latest_affiliations -t `ls -t1 $AFFILIATION_HOME/extracted_affiliations/input | head -n1`

deactivate