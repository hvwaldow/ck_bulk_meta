"""get_coordinates.py

Exatract coordinates and geographic names from csv file of the format

[city;country;latitude °N;longitude °E]

to CKAN format.

"""
import csv
import json

def get_coordinates(in_file):
    # coordinates = {'Type': 'Multipoint',
    #                'coordinates': []}
    coords = []
    geographic_name = []
    with open(in_file, 'r') as inf:
        reader = csv.reader(inf, delimiter=';')
        _ = reader.__next__()
        for row in reader:
            coords.append([float(row[3]), float(row[2])])
            geographic_name.append('{} ({})'.format(row[0], row[1]))
    spatial = json.dumps({'type': 'MultiPoint',
               'coordinates': coords})
    return (spatial, geographic_name)




    
