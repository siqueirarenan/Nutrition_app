"""
Django settings for Nutrition_app project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
"""
CONFIGURATION COMMANDS

- For running locally with Heroku:
python manage.py collectstatic
heroku local web -f Procfile.windows

- if collectstatic fails:
heroku config:set DEBUG_COLLECTSTATIC=1

- before deployment
manage.py check --deploy
"""

import django_heroku
import os
import psycopg2
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #for heroku?


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
f = open(os.path.join(BASE_DIR,"nutrition_app/key.txt"),'r')
key = f.readlines()
f.close()
SECRET_KEY = key[0]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True     #TODO: DEV ONLY
ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = ["localhost", "127.0.0.1",".herokuapp.com"]

ADMINS = [('renansiqueira', 'renansiqueira@gmail.com')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.sites',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ajax',
    'crispy_forms',
    'rest_framework',
    'Main',

   # 'sslserver', #TODO: DEV ONLY
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',            #to manage static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   #prevent clickjacking
]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
#X_FRAME_OPTIONS = 'SAMEORIGIN'
ROOT_URLCONF = 'nutrition_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'nutrition_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# To connect to database through CLI
# heroku pg:psql --app reset-challenge
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.postgresql_psycopg2',
#          'NAME': 'd70b90u9f6om4h',
#          'USER': 'kpxrkzhcjvwaca',
#          'PASSWORD': 'c8432332aaaf015c02045f817d923341c43b038035c6e57abe118a170a2fce59',
#          'HOST': 'ec2-34-232-24-202.compute-1.amazonaws.com',
#          'PORT': '5432',
#      }
#  }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nutrition',
        'USER': 'postgres',
        'PASSWORD': 'raquoasi',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'   #Is what goes to the static tag in the HTML inside the app
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #for Heroku

# Activate Django-Heroku.
django_heroku.settings(locals())

#Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Admin - Marcela Siqueira <acessoria.marcelasiqueira@gmail.com>'
#SERVER_EMAIL = 'acessoria.marcelasiqueira@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'acessoria.marcelasiqueira@gmail.com'
EMAIL_HOST_PASSWORD = key[1]
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 4 #TODO: in production, change to 5(?)
LOGIN_REDIRECT_URL = '/dashboard'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        #'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    }
}

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True