from project.settings.base import *

print("Loading development version")
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS.extend(['debug_toolbar'])
MIDDLEWARE.extend(['debug_toolbar.middleware.DebugToolbarMiddleware'])

# KeyRock Authentication
OAUTH_SERVER_BASEURL = 'https://test.naiades-project.eu:3443'
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"

DEBUG=True