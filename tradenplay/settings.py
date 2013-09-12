# Django settings for ASKBOT enabled project.
import os.path
import logging
import sys
import askbot
import site

# fake trans
ugettext = _ = lambda s: s

from .private_settings import *
# This is an utility function for accessing project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
path = lambda name: os.path.abspath(os.path.join(PROJECT_ROOT, name))

# this line is added so that we can import pre-packaged askbot dependencies
ASKBOT_ROOT = os.path.abspath(os.path.dirname(askbot.__file__))
site.addsitedir(os.path.join(ASKBOT_ROOT, 'deps'))


DEBUG = True  # set to True to enable debugging
TEMPLATE_DEBUG = True  # keep false when debugging jinja2 templates
ENABLE_SSL = False
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tradenplay',                      # Or path to database file if using sqlite3.
        'USER': 'tradenplay',                      # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# outgoing mail server settings
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_USE_TLS = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# incoming mail settings
# after filling out these settings - please
# go to the site's live settings and enable the feature
#"Email settings" -> "allow asking by email"
#
#   WARNING: command post_emailed_questions DELETES all
#            emails from the mailbox each time
#            do not use your personal mail box here!!!
#
IMAP_HOST = ''
IMAP_HOST_USER = ''
IMAP_HOST_PASSWORD = ''
IMAP_PORT = ''
IMAP_USE_TLS = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'ru'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    path('locale'),
    'ru/LC_MESSAGES/django.po',
)

CANONICAL_URL_HOST = 'tradenplay.com'
CANONICAL_URLS_TO_REWRITE = ['www.tradenplay.com', 'www.tradenplay.com.ua']
LOGIN_REDIRECT_URL = '/accounts/my_account'
# Absolute path to the directory that holds uploaded media
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'media'))
MEDIA_URL = '/media/'
# MEDIA_ROOT_URL = '/media/'
STATIC_URL = '/static/'  # this must be different from MEDIA_URL
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# Where and how the images will be stored
IMG_UPLD_DIR = 'upfiles'


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Make up some unique string, and don't share it with anybody.
SECRET_KEY = SECRET_KEY 

# List of callables that know how to import templatesus from various sources.
TEMPLATE_LOADERS = (
    'askbot.skins.loaders.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (

    #'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'askbot.middleware.locale.LocaleMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.sqlprint.SqlPrintingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    # below is askbot stuff for this tuple
    'askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'askbot.middleware.forum_mode.ForumModeMiddleware',
    'askbot.middleware.cancel.CancelActionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'askbot.middleware.view_log.ViewLogMiddleware',
    'askbot.middleware.spaceless.SpacelessMiddleware',


    'tradenplay.SSLMiddleware.SSLRedirect',
    'marketing.urlcanon.URLCanonicalizationMiddleware',
)


ROOT_URLCONF = os.path.basename(os.path.dirname(__file__)) + '.urls'


# UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(
    os.path.dirname(__file__),
    'tmp'
).replace('\\', '/')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = (
    '.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024  # result in bytes
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


TEMPLATE_DIRS = (
    path('templates'),
)


FIXTURE_DIRS = (
    path('fixtures'),
)
# This is a directory where all custom styling should be passed
ASKBOT_EXTRA_SKINS_DIR = os.path.abspath(
    os.path.join(STATIC_ROOT, 'custom_skins'))
# take a look here http://askbot.org/en/question/207/


THUMBNAIL_SIZE = (300, 180)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'askbot.context.application_settings',
    'django.core.context_processors.i18n',
    'askbot.user_messages.context_processors.user_messages',
    # must be before auth
    'django.contrib.auth.context_processors.auth',
    # this is required for the admin app
    'django.core.context_processors.csrf',  # necessary for csrf protection
    'utils.context_processors.project_constants'  # access your constants anwhr
)


INSTALLED_APPS = (
    'longerusername',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    # all of these are needed for the askbot
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'debug_toolbar',
    # Optional, to enable haystack search
    #'haystack',
    'askbot',
    'askbot.deps.django_authopenid',
    # 'askbot.importers.stackexchange', #se loader
    'south',
    'askbot.deps.livesettings',
    'keyedcache',
    'robots',
    'django_countries',
    'djcelery',
    'djkombu',
    'followit',
    'tinymce',
    'group_messaging',

    # Online store specific.
    # Third party.
    'tagging',   # https://pypi.python.org/pypi/django-tagging-ext/0.3.5
    'endless_pagination',
    # Custom build.
    'catalog',
    'cart',
    'checkout',
    'accounts',
    'search',
    'stats',
    # 'avatar',#experimental use git clone git://github.com/ericflo/django-avatar.git$

)


# setup memcached for production use!
# see http://docs.djangoproject.com/en/1.1/topics/cache/ for details
# CACHE_BACKEND = 'memcached://127.0.0.1:11211'
# needed for django-keyedcache
CACHE_TIMEOUT = 10
# sets a special timeout for livesettings if you want to make them different
LIVESETTINGS_CACHE_TIMEOUT = CACHE_TIMEOUT
# CACHE_PREFIX = 'askbot' #make this unique
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
# If you use memcache you may want to uncomment the following line to enable memcached based sessions
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': CACHE_TIMEOUT,
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'askbot.deps.django_authopenid.backends.AuthBackend',
)

# logging settings
LOG_FILENAME = 'askbot.log'
logging.basicConfig(
    filename=os.path.join(PROJECT_ROOT, 'log', LOG_FILENAME),
    level=logging.CRITICAL,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)

#
#
#   this will allow running your forum with url like http://site.com/forum
#
#   ASKBOT_URL = 'forum/'
#
ASKBOT_URL = 'forum/'  # no leading slash, default = '' empty string
ASKBOT_TRANSLATE_URL = True  # translate specific URLs
_ = lambda v: v  # fake translation function for the login url
LOGIN_URL = '/%s%s%s' % (ASKBOT_URL, _('account/'), _('signin/'))
LOGIN_REDIRECT_URL = ASKBOT_URL  # adjust, if needed
# note - it is important that upload dir url is NOT translated!!!
# also, this url must not have the leading slash
ALLOW_UNICODE_SLUGS = False
ASKBOT_USE_STACKEXCHANGE_URLS = False  # mimic url scheme of stackexchange

# Celery Settings
BROKER_TRANSPORT = "djkombu.transport.DatabaseTransport"
CELERY_ALWAYS_EAGER = True

import djcelery
djcelery.setup_loader()
DOMAIN_NAME = ''

CSRF_COOKIE_NAME = '_csrf'
# https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/
# CSRF_COOKIE_DOMAIN = DOMAIN_NAME

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATICFILES_DIRS = (
    ('default/media', os.path.join(ASKBOT_ROOT, 'media')),
    ASKBOT_EXTRA_SKINS_DIR,
)

RECAPTCHA_USE_SSL = True

# HAYSTACK_SETTINGS
ENABLE_HAYSTACK_SEARCH = False
HAYSTACK_SITECONF = 'askbot.search.haystack'
# more information
# http://django-haystack.readthedocs.org/en/v1.2.7/settings.html
HAYSTACK_SEARCH_ENGINE = 'simple'

TINYMCE_COMPRESSOR = True
TINYMCE_SPELLCHECKER = False
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'default/media/js/tinymce/')
TINYMCE_URL = STATIC_URL + 'default/media/js/tinymce/'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'convert_urls': False,
    'theme': 'advanced',
    'content_css': STATIC_URL + 'default/media/style/tinymce/content.css',
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': '',
    'mode': 'textareas',
    'oninit': "function(){ tinyMCE.activeEditor.setContent(askbot['data']['editorContent'] || ''); }",
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_buttons1': 'bold,italic,underline,|,bullist,numlist,|,undo,redo,|,link,unlink,askbot_imageuploader,askbot_attachment',
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3': '',
    'theme_advanced_path': False,
    'theme_advanced_resizing': True,
    'theme_advanced_resize_horizontal': False,
    'theme_advanced_statusbar_location': 'bottom',
    'width': '723',
    'height': '250'
}

# delayed notifications, time in seconds, 15 mins by default
NOTIFICATION_DELAY_TIME = 60 * 15

GROUP_MESSAGING = {
    'BASE_URL_GETTER_FUNCTION': 'askbot.models.user_get_profile_url',
    'BASE_URL_PARAMS': {'section': 'messages', 'sort': 'inbox'}
}
# Debug toolbar setup.
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
)

# Session timing(global_settings.py overrride)
SESSION_AGE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_AGE_DAYS

# Authorize.net credentials
AUTHNET_POST_URL = AUTHNET_POST_URL 
AUTHNET_POST_PATH = AUTHNET_POST_PATH 
AUTHNET_LOGIN = AUTHNET_LOGIN 
AUTHNET_KEY = AUTHNET_KEY 

AUTH_PROFILE_MODULE = 'accounts.userprofile'


# Pagination stuff
PAGINATE_BY = 20
# Number of products in crosselling's relevant products row
PRODUCTS_PER_ROW = 4

# Endless pagination module(ajax pagination)
ENDLESS_PAGINATION_PER_PAGE = 5
