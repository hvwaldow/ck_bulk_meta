"""find_res.py

Searches for particular resources.

Usage:
  find_res.py FN SEARCH
  find_res.py -h

Arguments:
  FN        a regular expression being matched against the field names.
  SEARCH    a regular expression being matched against field content.

Options:
  -h     Show this help.

"""

import ckanapi
from docopt import docopt
import sys
import os
import re


class res_find():
    def __init__(self, args):
        self.field = re.compile(args['FN'])
        self.search = re.compile(args['SEARCH'])
        self.ckan = self._getconn(); print(self.ckan)

    def _getconn(self):
        try:
            apikey = os.environ['CKAN_APIKEY_PROD1']
        except:
            apikey = None
        conn = ckanapi.RemoteCKAN(
            'https://data.eawag.ch', apikey)
        print(apikey)
        return conn

    def _get_pkg_generator(self):
        allpkgs = self.ckan.call_action('package_list')
        def return_pkg():
            for pkgname in allpkgs:
                res = self.ckan.call_action('package_show', {'id': pkgname})
                yield res
        return return_pkg()

    def _filter_resources(self, resources):
        for r in resources[0:1]:
            fieldfil = {k: r[k] for k in r if re.match(self.field, str(k))}
            valuefil = {k: r[k] for k in fieldfil if re.match(self.search, str(r[k]))}
            return valuefil
    
    def resources_find(self):
        results = {}
        for pkg in self._get_pkg_generator():
            resources = pkg.get('resources')
            if resources:
                resfil = self._filter_resources(resources)
                if resfil:
                    ### HIER weiter
                    results.update({pkg['name']] = resfil
            else:
                print('WARNING: {} has no resources.'.format(pkg['name']))
                next
        return results                                                                   
                                  
if __name__ == "__main__":
    args = docopt(__doc__, argv=sys.argv[1:])
    rf = res_find(args)
    results = rf.resources_find()
    print(results)
