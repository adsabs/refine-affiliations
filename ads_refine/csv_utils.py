"""
Functions to deal with CSV escape and unescape.
See: http://en.wikipedia.org/wiki/Comma-separated_values
"""

def escape_csv(data):
    if '"' in data:
        return '"%s"' % data.replace('"', '""')
    else:
        return data

def unescape_csv(data):
    if data.startswith('"') and data.endswith('"'):
        return data[1:-1].replace('""', '"')
    else:
        return data
