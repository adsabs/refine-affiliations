#!/bin/bash

celery worker --loglevel=WARNING &

echo "$!" > "celery.pid"

sleep 2