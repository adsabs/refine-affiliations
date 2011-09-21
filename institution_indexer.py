import os
import re
import solr
import time
import urllib2

import invenio.bibrecord as bibrecord

from config import solr_url, http_user, http_pass

CONNECTION = solr.SolrConnection(solr_url, http_user=http_user, http_pass=http_pass)

INDEX_FIELDS = {
        'institution': ['110__a', '110__t', '110__u', '110__x', '410__a', '410__g'],
        'department': ['110__b'],
        'address': ['371__a'],
        'city': ['371__b'],
        'state': ['371__c'],
        'country': ['371__d'],
        'zip_code': ['371__e'],
        'country_code': ['371__g'],
        }

def get_institution_marcxml():
    """
    Downloads the Inspire institution database.
    """
    marcxml = download_institution_chunk(0)
    out = open('etc/institutions_000.xm', 'w')
    out.write(marcxml)
    out.close()

    match = re.search('<!-- Search-Engine-Total-Number-Of-Results: (\d+) -->', marcxml)
    number_of_results = int(match.group(1))
    number_of_chunks = number_of_results / 200 + 1

    for i in range(1, number_of_chunks):
        marcxml = download_institution_chunk(i)
        out = open('etc/institutions_%03d.xm' % i, 'w')
        out.write(marcxml)
        out.close()

def download_institution_chunk(chunk_number, chunk_size=200):
    jrec = chunk_size * chunk_number + 1
    request = urllib2.Request('http://inspirebeta.net/search?cc=Institutions&jrec=%d&rg=%d&of=xm' % (jrec, chunk_size), headers={'User-Agent': 'Benoit Thiell, SAO/NASA ADS'})
    response = urllib2.urlopen(request)
    marcxml = response.read()
    response.close()
    return marcxml

def get_institution_records(path):
    """
    Returns all institution records in a BibRecord structure.
    """
    return [res[0] for res in bibrecord.create_records(open(path).read())]

def index_records(records):
    """
    Indexes all the institution records and then commits.
    """
    CONNECTION.add_many([get_indexable_data(record) for record in records])

def get_indexable_data(record):
    """
    Returns indexable data for a Bibrecord institution record in Solr.
    """
    # Mapped from https://twiki.cern.ch/twiki/bin/view/Inspire/DevelopmentRecordMarkupInstitutions#Field_Mapping_final
    data = {}

    data['id'] = bibrecord.record_get_field_value(record, '001')

    for index, tags in INDEX_FIELDS.items():
        values = []
        for tag in tags:
            for value in bibrecord.record_get_field_values(record, tag[:3],
                    tag[3], tag[4], tag[5]):
                values.append(value.decode('utf-8'))
        if values:
            data[index] = list(set(values))

    return data

if __name__ == '__main__':
#   print time.asctime() + ': Delete all previous institution files.'
#   for path in os.listdir('etc'):
#       os.remove('etc/' + path)
#   print time.asctime() + ': Download the Inspire institution database.'
#   get_institution_marcxml()
    print time.asctime() + ': Indexing in Solr.'
    for path in sorted(os.listdir('etc')):
        print time.asctime() + ': File %s.' % path
        records = get_institution_records('etc/' + path)
        index_records(records)
    CONNECTION.commit()
