"""get_authors.py

Exatract authors from csv file of the format

[Institution,First name,Middle initial,Last name,Email,City,Country,
Department,Street]

to a CKAN author - list.

Usage:
  get_authors.py [-h] [--affilmap] [-o <outfile>] <authorfile>

Options:
  -h --help              Show this help
  --affilmap             Produce a mapping author -> institution
  -o --output <outfile>  Write to <outfile> 

"""
from docopt import docopt
import csv
import sys
import json

def get_authors(in_file):
    authlist = []
    with open(in_file, 'r') as inf:
        reader = csv.reader(inf)
        _ = reader.__next__()
        for row in reader:
            authlist.append(_mk_author_string(row))
    authlist.sort(key=lambda L: (L.lower(), L))
    authlist = _custom_sort(authlist)
    return authlist

def get_affilmap(in_file):
    affilmap = {}
    with open(in_file, 'r') as inf:
        reader = csv.reader(inf)
        _ = reader.__next__()
        for row in reader:
            affilmap[_mk_author_string(row, strip_email=True)] = _mk_affil(row)
    return affilmap

def _mk_affil(row):
    dept = '' if row[7] == 'NA' else ', {}'.format(row[7])
    inst_dept = '{}{}'.format(row[0], dept)
    affil = '{}, {}, {}'.format(inst_dept, row[5], row[6])
    return affil
    
def _mk_author_string(row, strip_email=False):
    middle = '' if row[2] == 'NA' else ' {}'.format(row[2])
    if strip_email:
        return '{}, {}'.format(row[3], row[1] + middle)
    else:
        return '{}, {} <{}>'.format(row[3], row[1] + middle, row[4])

def _custom_sort(authlist):
    authlist.insert(0, authlist.pop(64)) # Ort first author
    authlist.insert(64, authlist.pop(91)) # Östmann after Oertel
    return authlist

if __name__ == '__main__':
    args = docopt(__doc__, sys.argv[1:], help=True)
    print(args)
    in_file = args['<authorfile>']
    if args['--affilmap']:
        result = get_affilmap(in_file)
    else:
        result = get_authors(in_file)
    if args['--output']:
        with open(args['--output'], 'w') as outfile:
            outfile.write(json.dumps(result, indent=4))
    else:
        print(result)


    
