#!/bin/bash -xe

AFFILIATION_HOME=`pwd`

source $AFFILIATION_HOME/python/bin/activate

python scripts/institution_indexer.py --download

deactivate