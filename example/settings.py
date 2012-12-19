# Django settings for example project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'example.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# A list of locations of additional static files
STATICFILES_DIRS = (
        os.path.join(os.path.dirname(__file__), 'static_media'),
        )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
   #'django.contrib.staticfiles.finders.DefaultStorageFinder',
   'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'
FEINCMS_ADMIN_MEDIA = '/media/feincms/'

SECRET_KEY = '_wn95s-apfd-442cby5m^_^ak6+5(fyn3lvnvtn7!si&o)1x^w'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'feincmsext.simple_permission.backend.SimplePagePermissionBackend',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'feincms',
    'feincms.module.blog',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'example',

    'django.contrib.admin',

    'mptt',
    
    'feincmsext.extended_navigation',
    'feincmsext.util',
    'feincmsext.simple_permission',
)

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    )

FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = False
FEINCMS_TREE_EDITOR_OBJECT_PERMISSIONS = True
