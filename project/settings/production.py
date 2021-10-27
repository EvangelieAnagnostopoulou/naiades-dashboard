from project.settings.base import *

print("Loading production version")


# KeyRock Authentication
OAUTH_SERVER_BASEURL = 'https://test.naiades-project.eu:3443'
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE.append(
     'whitenoise.middleware.WhiteNoiseMiddleware',
)

# SSl settings
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
