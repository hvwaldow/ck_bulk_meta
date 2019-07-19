"""update_coordinates.py

Updates a package's spatial coordinates (just
MultiPoint implemented) and geographic names with those taken from a csv file
with the format:

[city;country;latitude °N;longitude °E]

Usage:
  update_coordinates.py <coord_file> <pkg_url>

Arguments:
   <coord_file>    input file
   <pkg_url>   The URL of the package in CKAN

"""
from docopt import docopt
import ckanapi as ck
import os

APIKEY = os.environ['CKAN_APIKEY_PROD1']
COORDFILE = 'SCORE_coordinates_repository_conv.csv'
#URL = 'https://data.eawag.ch/dataset/illicit-drugs-in-wastewater-score-initiative'
URL = https://data.eawag.ch/dataset/edit/a-test-for-usability


