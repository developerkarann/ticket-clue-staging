from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

UNIVERSAL_AIR_API_BASE_URL = os.getenv('UNIVERSAL_AIR_API_BASE_URL')
UNIVERSAL_AIR_API_BOOK_URL = os.getenv('UNIVERSAL_AIR_API_BOOK_URL')

UNIVERSAL_AIR_API_AUTH_URL = os.getenv('UNIVERSAL_AIR_API_AUTH_URL')        

TRAVEL_BOUTIQUE_CLIENT_ID = os.getenv('TRAVEL_BOUTIQUE_CLIENT_ID')
TRAVEL_BOUTIQUE_USERNAME = os.getenv('TRAVEL_BOUTIQUE_USERNAME')
TRAVEL_BOUTIQUE_PASSWORD = os.getenv('TRAVEL_BOUTIQUE_PASSWORD')

RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

# Optional: external airport search API (if set, search_airports tries this before DB)
AIRPORT_API_URL = os.getenv('AIRPORT_API_URL')  # e.g. https://your-api.com/airports
AIRPORT_API_QUERY_PARAM = os.getenv('AIRPORT_API_QUERY_PARAM', 'q')

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000","http://ticketclue.com","https://ticketclue.com"]


# Use SQLite for local dev when USE_SQLITE=True (no PostgreSQL needed)
_use_sqlite = os.getenv('USE_SQLITE', '').lower() in ('true', '1', 'yes')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3' if _use_sqlite else 'django.db.backends.postgresql',
        'NAME': BASE_DIR / 'db.sqlite3' if _use_sqlite else os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),  # updated username
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),      # ensure this matches the role’s password (if one is set)
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookings',
    'home',
    'accounts',
    'flights',
    'orders',
    'import_export',
    'widget_tweaks',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flightApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.airlines_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'flightApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 # higher than the count of fields


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
