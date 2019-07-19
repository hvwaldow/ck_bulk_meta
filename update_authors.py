"""update_authors.py

Updates package's author list with the one read from a csv file with the
format:
[Institution,First name,Middle initial,Last name,Email,City,Country,
Department,Street]

Usage:
  update_authors.py <author_file> <pkg_url>

Arguments:
  <author_file> input file
  <pkg_url> The URL of the package in CKAN

"""
from docopt import docopt
import ckanapi as ck
import os
import re
import get_authors
import importlib
importlib.reload(get_authors)
import get_coordinates
importlib.reload(get_coordinates)


APIKEY = os.environ['CKAN_APIKEY_PROD1']
#INFILE = 'authors_SCORE_data_2011_2017_final_Form_Responses_1.csv'
INFILE = 'SCORE_coordinates_repository_conv.csv'
URL = 'https://data.eawag.ch/dataset/illicit-drugs-in-wastewater-score-initiative'
#URL = 'https://data.eawag.ch/dataset/edit/a-test-for-usability'

def _get_conn(url):
    host = re.match(r'(https?://.*?)/.*', url).group(1)
    return ck.RemoteCKAN(host, apikey=APIKEY)

def _get_pkgname(url):
    pkgname = re.match(r'https?://.*/(.*)', url).group(1)
    return pkgname
    
def get_pkg(url, conn, pkgname):
    pkg = conn.call_action('package_show', data_dict={'id': pkgname})
    return(pkg)

def update_pkg(conn, pkg):
    conn.call_action('package_update', data_dict=pkg)

url = URL
conn =  _get_conn(url)
pkgname = _get_pkgname(url)
pkg = get_pkg(url, conn, pkgname)
#pkg.update({'author': get_authors.get_authors(INFILE)})
spatial, geographic_name = get_coordinates.get_coordinates(INFILE)
pkg.update({'spatial': spatial})
pkg.update({'geographic_name': geographic_name})
update_pkg(conn, pkg)


    

