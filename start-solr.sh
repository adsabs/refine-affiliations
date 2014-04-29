#!/bin/bash

cd solr

java -jar start.jar &
pid=$!

cd ..
echo "$!" > solr.pid
