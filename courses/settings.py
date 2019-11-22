import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

DEBUG = bool(int(os.environ.get("DEBUG", 1)))

db_service_name = os.getenv('DATABASE_SERVICE_NAME', '')
db_name = os.getenv('{}_DATABASE'.format(db_service_name.upper()), 'courses')
db_user = os.getenv('{}_USER'.format(db_service_name.upper()), '')
db_pwd = os.getenv('{}_PASSWORD'.format(db_service_name.upper()), '')
db_host = os.getenv('{}_SERVICE_HOST'.format(db_service_name.upper()), 'localhost')
db_port = os.getenv('{}_SERVICE_PORT'.format(db_service_name.upper()), '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_pwd,
        'HOST': db_host,
        'PORT': db_port,
    }
}

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DATETIME_INPUT_FORMATS = ["%Y-%m-%d %I:%M %p"]

ROOT_URLCONF = "courses.urls"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "static", "dist")]

if "test" not in sys.argv:
    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "p$13e+mc+5o)h7zi)4$txl3=46vjcevqegfe5uxe8=vecx!5%0"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PACKAGE_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
                "pinax_theme_bootstrap.context_processors.theme",
            ],
        },
    }
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG and bool(int(os.environ.get("RUN_DDT", 1))):
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "courses.wsgi.application"

INSTALLED_APPS = [
    "courses_theme",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # theme
    "bootstrapform",
    "django_forms_bootstrap",
    "pinax_theme_bootstrap",
#    "pinax.eventlog",
    "taggit",

    # external
    "account",
    "django_tables2",
    "h5pp",
 
    # project
    "h5p",
    "courses",
]

if DEBUG and bool(int(os.environ.get("RUN_DDT", 1))):
    INSTALLED_APPS += ["debug_toolbar"]


# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
DEFAULT_LOG_LEVEL = "INFO"
if DEBUG:
    DEFAULT_LOG_LEVEL = "DEBUG"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [os.path.join(PROJECT_ROOT, "fixtures")]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_URL = 'learner_login'
ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "learner_course_list"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True


AUTHENTICATION_BACKENDS = [
    "account.auth_backends.UsernameAuthenticationBackend",
]

H5P_VERSION = '7.x'
H5P_DEV_MODE = 0
H5P_PATH = os.path.join(BASE_DIR, 'h5pp/static/h5p')
H5P_URL = '/h5p/'
H5P_SAVE = 30
H5P_EXPORT = '/exports/'
H5P_LANGUAGE = 'en'
