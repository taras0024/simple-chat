# -----------------------------------------------------------------------------
# Applications definition
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Admin tools
    'jazzmin',
    'dal',
    'dal_select2',

    # Django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party modules
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',

    # Local apps located at backend.apps.*
    'db.users',
    'db.chats',

    'service',
    'api',
]
