#!/bin/bash -xe

AFFILIATION_HOME=`pwd`

source $AFFILIATION_HOME/python/bin/activate

export RABBITMQ_NODE_PORT=5673
./rabbitmq-server/sbin/rabbitmq-server -detached
./rabbitmq-server/sbin/rabbitmqctl status

sleep 2


celery worker --loglevel=WARNING &

echo "$!" > "celery.pid"

sleep 2



# This runs the disambiguation with the latest file extracted.
python $AFFILIATION_HOME/ads_refine/disambiguate.py -e $AFFILIATION_HOME/extracted_affiliations/input/`ls -t1 $AFFILIATION_HOME/extracted_affiliations/input/ | head -n1` "Astronomy affiliations disambiguation"

echo "After disambiguation"

# stop celery
kill `cat celery.pid`

# stop rabbitmq
./rabbitmq-server/sbin/rabbitmqctl stop
