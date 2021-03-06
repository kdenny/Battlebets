"""
Django settings for yelphackathon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'is#97k(u_srvfq*$@+ur9g+1v8j5t#rt(d4-14^0mzql&2lugj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['kdenny37.pythonanywhere.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kombu.transport.django',
    'bbapp',
    'bootstrapform',
    'leaflet'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django_openid_consumer.SessionConsumer',
)

ROOT_URLCONF = 'Battlebets.urls'

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'



SITE_ID = 1

WSGI_APPLICATION = 'Battlebets.wsgi.application'

# SERIALIZATION_MODULES = {
#     'geojson' : 'djgeojson.serializers'
# }

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT = "/home/kdenny37/yelphackathon/static"

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=bettr/scripts',
]

CORS_ORIGIN_ALLOW_ALL = True

############
#   KEYS   #
############

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kdenny37@gmail.com'
EMAIL_HOST_PASSWORD = 'kedeezy37'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_PORT = 587

TWITTER_CONSUMER_KEY = 'BEV7sVDMKhzm7kEDftKMxcMLN'
TWITTER_CONSUMER_SECRET = 'FOGALJXgVSa3pOleExbS6tZRsi2keDoOutofq6NYWpYoApjvpC'
TWITTER_ACCESS_TOKEN = '418156887-Lkwj44RsSQQJPWPkJcHRwA0aKfvFhMDNlIuOTun3'
TWITTER_ACCESS_TOKEN_SECRET = '	FRrjiig9A46nnEy5VDsQ7Jxyc533vkq13gvQxG0QBypHA'

LINKEDIN_CLIENT_ID = '77uu0uetayvmx1'
LINKEDIN_CLIENT_SECRET = 'xKw6QWVetdSCjM98'

YELP_CONSUMER_KEY = '0tUp7UtWTfanw6MDaZtduA'
YELP_CONSUMER_SECRET = 'rDmAHimMH4OfCDtkmM-MaYgBWjc'
YELP_TOKEN = 'qLMFQgP8T1bg9FBawvA7_XSm_HBUU_fi'
YELP_TOKEN_SECRET = '7u4Z639XXHFjR9juqfmyPxEhLWI'

##  NYT API keys
POPAPIKEY = 'ab386acd8529d2218fd793a874342d14:19:69591235'
TOPAPIKEY = '88ac43a6334b0e3990bd9739b5d866e1:8:69591235'

FACEBOOK_APP_ID = '634346716713278'
FACEBOOK_APP_SECRET = 'bbd6042a0cccaf318e1a4b56dede8877'