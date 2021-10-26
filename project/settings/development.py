from project.settings.base import *

import dj_database_url
# DATABASES['default'] =  dj_database_url.config()
#updated
DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}
