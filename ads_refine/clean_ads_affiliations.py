import codecs
import os
import re
import sys

assert sys.hexversion >= 0x02060000

from csv_utils import escape_csv

try:
    import ads.Unicode
except ImportError:
    sys.path.append('/proj/ads/soft/python/lib/site-packages')
    import ads.Unicode

UNICODE_HANDLER = ads.Unicode.UnicodeHandler()
SPACES_REGEX = re.compile('\s+')

def _preclean_affiliation(aff):
    """
    Performs basic cleaning operations on an affiliation string.
    """
    aff = SPACES_REGEX.sub(' ', aff).strip()
    aff = UNICODE_HANDLER.ent2u(aff.decode('utf-8'))
    return aff

def clean_ads_affs(path, verbose=0):
    """
    Reads an ADS affiliation file in the form:
    bibcode\taffiliation

    Returns a file in the form:
    affiliation\tbibcode1 bibcode2
    """
    txt = open(path).read()

    msg('-- Create the list of bibcodes.', verbose)

    lines = [line.split('\t', 2) for line in txt.split('\n') if line]
    lines = [
            [bibcode + ',' + position, _preclean_affiliation(escape_csv(line))]
            for bibcode, position, line in lines
            ]

    # Reverse dictionary
    d = {}
    for bibcode, line in lines:
        d.setdefault(line, []).append(bibcode)

    msg('-- Transform back to list', verbose)
    d = sorted(d.items())

    if path.endswith('.merged'):
        new_path = os.path.join('/tmp', os.path.basename(path)[:-7] + '.reversed')
    else:
        new_path = os.path.join('/tmp', os.path.basename(path) + '.reversed')

    msg('-- Writing to file %s.' % new_path, verbose)

    d = sorted(['\t'.join([aff, ' '.join(bibcodes)]) for aff, bibcodes in d])
    codecs.open(new_path, mode='w', encoding='utf-8').write('\n'.join(d))
    msg('-- Done writing to file.', verbose)

    return new_path

def msg(message, verbose):
    if verbose:
        print message
