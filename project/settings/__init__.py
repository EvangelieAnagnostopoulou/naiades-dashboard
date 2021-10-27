import os


print("Environment",os.environ.get('ENVIRONMENT', ''))

if os.environ.get('ENVIRONMENT', '') == 'PRODUCTION':
    from project.settings.production import *
else:
    from project.settings.development import *
