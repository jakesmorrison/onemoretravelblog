"""
WSGI config for onemoretravelblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os, sys, site

# add site dir
site.addsitedir('/root/.virtualenvs/jakobmorrison_env/lib/python3.5/site-packages/')

# Calculate the path based on the location of the WSGI script.
sys.path.append('/root/onemoretravelblog')
sys.path.append('/root/onemoretravelblog/onemoretravelblog')

# Add the path to 3rd party django application and to django itself.
#sys.path.append('/root')
os.environ['DJANGO_SETTINGS_MODULE'] = 'onemoretravelblog.apache.override'

activate_env='/root/.virtualenvs/jakobmorrison_env/bin/activate_this.py'
exec(open(activate_env).read())

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

