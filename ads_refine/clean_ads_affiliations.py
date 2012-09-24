import os
import re
import sys

assert sys.hexversion >= 0x02060000

from csv_utils import escape_csv
from collections import defaultdict

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
    aff = aff.decode('utf8')
    aff = SPACES_REGEX.sub(' ', aff).strip()
    aff = UNICODE_HANDLER.ent2u(aff)
    return aff

RE_EMAIL = re.compile('<EMAIL>(.*?)</EMAIL>')

def extract_emails(aff):
    emails = []
    for match in RE_EMAIL.finditer(aff):
        emails.append(match.group(1))

    aff = RE_EMAIL.sub(' ', aff)
    aff = re.sub('\s\s+', ' ', aff).strip()
    if '<EMAIL>' in aff or '</EMAIL>' in aff:
        raise Exception('Wrong email markup.')
    return aff, emails

def clean_ads_affs(path, verbose=0):
    """
    Reads an ADS affiliation file in the form:
    bibcode\taffiliation

    Returns a file in the form:
    affiliation\taffiliation\temails\temails\tbibcode1 bibcode2
    """
    msg('-- Create the list of bibcodes.', verbose)

    affiliations = defaultdict(list)

    for line in open(path):
        line = line.strip()
        # Sandwich.
        try:
            line = line.decode('utf8')
        except UnicodeDecodeError:
            print 'UNICODE ERROR:', line
            continue
        bibcode, position, affiliation = line.strip().split('\t', 2)
        try:
            affiliation = _preclean_affiliation(escape_csv(affiliation))
        except ads.Unicode.UnicodeHandlerError:
            print 'ENTITY ERROR:', line
            continue
        affiliations[affiliation].append('%s,%s' % (bibcode, position))

    msg('-- Transform back to list', verbose)
    affiliations = sorted(affiliations.items())

    if path.endswith('.merged'):
        new_path = os.path.join('/tmp', os.path.basename(path)[:-7] + '.reversed')
    else:
        new_path = os.path.join('/tmp', os.path.basename(path) + '.reversed')

    msg('-- Writing to file %s.' % new_path, verbose)

    out = open(new_path, 'a')
    out.write('Original affiliation\tNew affiliation\tOriginal emails\tNew emails\tBibcodes and positions\n')
    for affiliation, bibcodes in affiliations:
        try:
            affiliation, emails = extract_emails(affiliation)
        except Exception, exc:
            print 'WARNING: Wrong email markup: %s' % affiliation
        emails = [email.encode('utf_8') for email in emails]
        line = '%s\t%s\t%s\t%s\t%s\n' % (affiliation, affiliation, emails, emails, ' '.join(bibcodes))
        out.write(line.encode('utf_8'))
    out.close()

    msg('-- Done writing to file.', verbose)

    return new_path

def msg(message, verbose):
    if verbose:
        print message
