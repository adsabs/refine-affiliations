Affiliation disambiguation tool.

Usage:

   1. to setup the project
		``bash
		$ git clone https://github.com/adsabs/refine-affiliations
		$ cd refine-affiliations 
		$ ./setup.sh

    # if you want to run services locally, you need to start them

    $ ./start-solr.sh
    $ ./start-rabbitmq.sh
    $ ./start-celery.sh 
		``

    You can also use services running on the adsx machine; for this you have to edit

      * accounts.cfs
      * celeryconfig.py

    And set the following:

      accounts.cfg
        url = http://adsx.cfa.harvard.edu:8983/solr

      celeryconfig.py:
        BROKER_URL = "amqp://guest:guest@localhost:5674/"

   2. get data from Refine server (http://adsx:3333)
		``bash
		$ ./export-data-from-refine.sh 
		``
   3. extract affiliations from ADS Classic (this can be run only on machines with access to PERL libraries)
		``bash
		$ ./extract-ads-classic-affiliations.sh 
		``
   4. disambiguate affiliations 
		``bash 
    $ ./start-celery.sh
		$ ./disambiguate-affiliations.sh 
    $ ./stop-celery.sh
		``
   5. export affiliations back to Refine 
		``bash 
		$ ./export-data-into-refine.sh 
		``

Author: Benoit Thiell <bthiell@cfa.harvard.edu>
License: GPL

== Requirements ==

* Python 2.6+
* Solrpy (https://code.google.com/p/solrpy/)
* Celery (http://celeryproject.org/) is optional and allows to run the search with multiple processes.

== Examples ==

=== Return the best match ===

    In [1]: from institution_searcher import get_match

    In [2]: get_match('Center for Astrophysics, Cambridge, MA')
    Out[2]: (u'Harvard-Smithsonian Ctr. Astrophys., Cambridge', 0.39160477649239001)

The first value is the new ICN if it exists, or the ICN. The second value is the score of the match which is computed from the ratio between the score of the first and second item of the results list. The closer to 1, the better the score.

=== Get the full results ===

    In [1]: from institution_searcher import search_institution

    In [2]: search_institution('CERN')
    Out[2]: 
    [{u'display_name': u'CERN, Geneva',
      u'id': u'902725',
      u'score': 5.1152430000000004},
     {u'display_name': u'ECFA', u'id': u'905995', u'score': 2.5764835000000001},
     {u'display_name': u'UCT-CERN Res. Ctr.',
      u'id': u'910762',
      u'score': 2.0611868000000002}]