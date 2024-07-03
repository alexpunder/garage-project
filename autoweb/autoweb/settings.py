import os
from pathlib import Path

from django.contrib.messages import constants as messages
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') == 'True'

MAIN_BOT_TOKEN = os.getenv('MAIN_BOT_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('USER_TOKEN_ID')

AUTH_USER_MODEL = 'users.CustomUser'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

INTERNAL_IPS = ['127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://garage-vlz.ru']
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


TEMPLATES_DIR = BASE_DIR / 'templates'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_LOCATION', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')


DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3')

if DB_ENGINE == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'django'),
            'USER': os.getenv('POSTGRES_USER', 'django'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', ''),
            'PORT': os.getenv('DB_PORT', 5432),
        }
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_bootstrap5',
    'cachalot',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.google',

    'authorization.apps.AuthorizationConfig',
    'pages.apps.PagesConfig',
    'shop.apps.ShopConfig',
    'users.apps.UsersConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',

    'django_recaptcha',
    'django_filters',
    'phonenumber_field',
    'jquery',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'autoweb.urls'
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_context_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'autoweb.wsgi.application'


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


LANGUAGE_CODE = 'ru-RU'
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'RU'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'


LOGIN_URL = 'auth:login'
LOGIN_REDIRECT_URL = '/'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'autovlz@yandex.ru'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER


TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

SOCIALACCOUNT_PROVIDERS = {
    'yandex': {
        'APPS': [
            {
                'client_id': os.getenv('SOCIALACCOUNT_YANDEX_CLIENT_ID'),
                'secret': os.getenv('SOCIALACCOUNT_YANDEX_SECRET'),
                'key': os.getenv('SOCIALACCOUNT_YANDEX_KEY')
            },
        ],
        'SCOPE': [
            'login:default_phone',
            'login:info',
            'login:email'
        ]
    },
    'google': {
        'APPS': [
            {
                'client_id': os.getenv('SOCIALACCOUNT_GOOGLE_CLIENT_ID'),
                'secret': os.getenv('SOCIALACCOUNT_GOOGLE_SECRET'),
                'key': os.getenv('SOCIALACCOUNT_GOOGLE_KEY')
            },
        ],
        'SCOPE': [
            'profile',
            'email',
        ],
    },
}

SOCIALACCOUNT_LOGIN_ON_GET = True
