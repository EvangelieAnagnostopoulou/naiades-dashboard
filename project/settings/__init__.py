import os
import sys


if os.environ.get('ENVIRONMENT', '') == 'PRODUCTION':
    from project.settings.production import *
elif os.environ.get('ENVIRONMENT', '') == 'STAGING':
    from project.settings.staging import *
else:
    from project.settings.development import *
