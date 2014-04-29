#!/bin/bash -ev

# This task will setup the environment and also the necessary folder structure for running Affiliations
# necessary, otherwise it is using wrong python (?!)
unset PYTHONHOME

if [ -d python ]; then
  rm -fR python
fi

# create a virtual python
virtualenv --unzip-setuptools --no-site-packages python

source python/bin/activate

pip install -r requirements.txt

echo "Symlinking ads libraries; if this fails, you need to mount remote filesystem: sshfs adsx:/proj /proj"
ln -s /proj/ads/soft/python/lib/site-packages/ads python/lib/python2.7/site-packages/ads

deactivate

mkdir -p extracted_affiliations/input || 0
mkdir -p extracted_affiliations/output || 0

# celery needs rabbitmq, we'll run rabbitmq locally
if [ ! -d rabbitmq_server-3.0.4 ]; then
   wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.0.4/rabbitmq-server-generic-unix-3.0.4.tar.gz
   tar -xzf rabbitmq-server-generic-unix-3.0.4.tar.gz
   mv rabbitmq_server-3.0.4 rabbitmq-server
fi

if [ -f accounts.cfg ]; then 
	echo "[solr]
	url = http://localhost:8983/solr
	user = benoit
	password = anothersolrpassword

	[spreadsheet]
	user = badzil@gmail.com
	password = mtrfrswdktijnziu
	" > accounts.cfg
fi 


if [ ! -f celeryconfig.py ]; then 
	echo 'BROKER_URL = "amqp://guest:guest@localhost:5673/"
	CELERY_RESULT_BACKEND = "amqp"
	CELERY_IMPORTS = ("ads_refine.institution_searcher", )
	CELERYD_CONCURRENCY = 6' > celeryconfig.py
fi 


echo "Edit accounts.cfg|celeryconfig.py if you need to modify setup"

