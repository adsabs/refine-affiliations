#!/usr/bin/python26

import sys
assert sys.hexversion >= 0x02060000

from google.refine import refine

SERVER = 'http://adsx.cfa.harvard.edu:3333'

def main():
    r = refine.Refine(SERVER)
    for id, d1 in r.list_projects().items():
        if d1['name'].startswith('Test project'):
            r.open_project(id).delete()

if __name__ == '__main__':
    main()
