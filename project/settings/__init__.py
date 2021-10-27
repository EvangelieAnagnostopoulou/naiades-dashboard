import os


print(os.environ.get('ENVIRONMENT', ''))
if os.environ.get('ENVIRONMENT', '') == 'PRODUCTION':
    from project.settings.production import *
else:
    from project.settings.development import *
