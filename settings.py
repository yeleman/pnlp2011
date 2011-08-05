# Django settings for pnlp2011 project.

import os
import tempfile

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
TEMP_DIR = tempfile.gettempdir()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-w7%yno2dw@ix50u7@bve$rx0%!n+_5b^+^vyjv(zc=3(oa_44'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'babeldjango.middleware.LocaleMiddleware',
    'pnlp_web.middleware.Http500Middleware',
    'pnlp_web.middleware.Http404Middleware',
    'pnlp_web.middleware.Http403Middleware',
)

ROOT_URLCONF = 'pnlp2011.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # pnlp2011 specific apps
    'django.contrib.humanize',
    'babeldjango',
    'nosms',
    'bolibana_reporting',
    'bolibana_auth',
    'pnlp_core',
    'pnlp_sms',
    'pnlp_web',
    'reversion',
    'django_extensions',
    'south',
)

# Logging policy:
# debug on /tmp
# warning+ in ./logs/
# error+ triggers email to admin
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s ' \
                      '%(name)s/L%(lineno)d: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(TEMP_DIR, 'pnlp_debug.log'),
            'maxBytes': 1024 * 1024 * 2,  # 2MB
            'backupCount': 1
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'W0',
            'interval': 1,
            'backupCount': 8,
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'activity.log'),
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'debug', 'file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

DEFAULT_LOCALE = 'fr_FR.UTF-8'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SENDER = 'root@localhost'

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

NOSMS_HANDLER = 'pnlp_sms.palu.nosms_handler'
NOSMS_TRANSPORT_HOST = 'localhost'
NOSMS_TRANSPORT_PORT = 13013
#NOSMS_TRANSPORT_USERNAME = None
#NOSMS_TRANSPORT_PASSWORD = None

HOTLINE_NUMBER = "00000000"
HOTLINE_EMAIL = "root@localhost"

SUPPORT_CONTACTS = [('unknown', u"HOTLINE", HOTLINE_EMAIL)]

ENABLE_FORTUNE = True

USE_HTTPS = False

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "pnlp_web.context_processors.add_provider",
    "pnlp_web.context_processors.add_level")

AUTH_PROFILE_MODULE = 'bolibana_auth.Provider'

# loads custom settings from a separate file
try:
    from local_settings import *
except ImportError:
    pass
