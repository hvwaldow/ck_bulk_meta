"""rm_res_perms.py

Removes restrictions from all ressources of a package

Usage:
  rm_res_perms.py PKG
  rm_res_perms.py -h

Arguments:
  PKG       The package name or id

Options:
  -h     Show this help.

"""

import ckanapi
from docopt import docopt
from pprint import pprint
import sys
import os
import re

class ResPerms():
    def __init__(self, args):
        self.pkgnam = args['PKG']
        self.conn = self._getconn()

    def _getconn(self):
        try:
            apikey = os.environ['CKAN_APIKEY_PROD1']
            print("apikey found")
        except:
            print("No apikey found")
            apikey = None
        conn = ckanapi.RemoteCKAN('https://data.eawag.ch', apikey)
        return conn

    def _get_res(self):
        res = self.conn.call_action(
            'package_show',
            {'id': self.pkgnam}
        )['resources']
        return res
    
    def _rm_restrictions(self):
        for r in self._get_res():
            r['restricted_level'] = 'public'
            r['allowed_users'] = ''
            self.conn.call_action('resource_update', r)
            try:
                self.conn.call_action('resource_update', r)
            except:
                print('Error: Updating resource {} in package {} failed.'
                      .format(self.pkgnam, r['name']))

    def _list_perms(self):
        for r in self._get_res():
            for field in ['name', 'restricted_level', 'allowed_users']:
                print('    {}: {}'.format(field, r[field]))
                
    def main(self):
        print('')
        print('Modifying package {}'.format(self.pkgnam))
        print('Original restrictions:')
        self._list_perms()
        print('Modifying')
        self._rm_restrictions()
        print('New restrictions')
        self._list_perms()

if __name__ == "__main__":
    args = docopt(__doc__, argv=sys.argv[1:])
    rp = ResPerms(args)
    rp.main()
