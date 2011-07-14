import sys
import re
import os
import codecs
from csv_utils import escape_csv

sys.path.append('/proj/ads/soft/python/lib/site-packages')
import ads.Unicode

UNICODE_HANDLER = ads.Unicode.UnicodeHandler()
SPACES_REGEX = re.compile('\s+')

def _preclean_affiliation(aff):
    aff = SPACES_REGEX.sub(' ', aff).strip()
    aff = UNICODE_HANDLER.ent2u(aff.decode('utf-8'))
    return aff

def clean_ads_affs(path):
    txt = open(path).read()

    print '-- Create the list of bibcodes.'

    lines = [line.split('\t', 2) for line in txt.split('\n') if line]
    lines = [[bibcode + ',' + position, _preclean_affiliation(escape_csv(line))] for bibcode, position, line in lines]

    # Reverse dictionary
    d = {}
    for bibcode, line in lines:
        d.setdefault(line, []).append(bibcode)

    print '-- Transform back to list'
    d = sorted(d.items())

    if path.endswith('.merged'):
        new_path = os.path.join('/tmp', os.path.basename(path)[:-7] + '.reversed')
    else:
        new_path = os.path.join('/tmp', os.path.basename(path) + '.reversed')

    print '-- Writing to file %s.' % new_path

    d = sorted(['\t'.join([aff, ' '.join(bibcodes)]) for aff, bibcodes in d])
    codecs.open(new_path, mode='w', encoding='utf-8').write('\n'.join(d))
    print '-- Done writing to file.'

    return new_path
