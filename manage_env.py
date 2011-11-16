#!/usr/bin/env python

import sys
import site
import os

vepath = '/home/pnlp/src/envs/pnlp/lib/python2.6/site-packages'
if not os.path.exists(vepath):
    sys.stderr.write("Virtual Env not found.")

prev_sys_path = list(sys.path)

# add the site-packages of our virtualenv as a site dir
site.addsitedir(vepath)

sys.path.append('/home/pnlp/src/pnlp2011')

# reorder sys.path so new directories from the addsitedir show up first
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path


# regular manage code
from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings')  # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in " \
                     "the directory containing %r. It appears you've " \
                     "customized things.\nYou'll have to run " \
                     "django-admin.py, passing it your settings module.\n" \
                     % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
