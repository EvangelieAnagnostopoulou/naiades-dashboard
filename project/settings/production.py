from project.settings.base import *

print("Loading production version")

#SSl settings
#Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

DEBUG = os.environ.get("DEBUG_UNSAFE") == "ON"
