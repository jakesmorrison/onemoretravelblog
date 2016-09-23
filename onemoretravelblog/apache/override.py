#override.py

from onemoretravelblog.settings import *

DEBUG = True
ALLOWED_HOSTS = ['www.onemoretravelblog.com', '192.241.228.71']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "/root/database/db.sqlite3",
    }
}

