from project.settings.base import *

print("Loading development version")
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS.extend(['debug_toolbar'])
MIDDLEWARE.extend(['debug_toolbar.middleware.DebugToolbarMiddleware'])

DEBUG=True