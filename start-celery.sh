#!/bin/bash

AFFILIATION_HOME=`pwd`

source $AFFILIATION_HOME/python/bin/activate

celery worker --loglevel=WARNING &

echo "$!" > "celery.pid"

sleep 2

deactivate