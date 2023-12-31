import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='super_secret_key_513115%')

DEBUG = os.getenv('DEBUG', default='False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='*').split()

# SSL
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', default='').split()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_filters',
    'drf_spectacular',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'djoser',
    'mptt',
    'mdeditor',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'articles.apps.ArticlesConfig',
    'likes.apps.LikesConfig',
    'mailings.apps.MailingsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

CORS_ALLOW_ALL_ORIGINS = (
    os.getenv('CORS_ALLOW_ALL_ORIGINS', default='False').lower() == 'true'
)

ROOT_URLCONF = 'stethoscope.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stethoscope.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'stethoscope_db'),
        'USER': os.environ.get('POSTGRES_USER', 'stethoscope_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'stethoscope_password'),
        'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        },
    },
    {
        'NAME': 'users.validators.PasswordMaximumLengthValidator',
        'OPTIONS': {
            'max_length': 20,
        },
    },
    {
        'NAME': 'users.validators.PasswordCharactersNotAllowedValidator',
        'OPTIONS': {
            'excluded_characters': ' ',  # space by default
        },
    },
]

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

CURSOR_PAGINATION_PAGE_SIZE = int(os.getenv('CURSOR_PAGINATION_PAGE_SIZE', default=6))
CURSOR_PAGINATION_MAX_PAGE_SIZE = int(
    os.getenv('CURSOR_PAGINATION_MAX_PAGE_SIZE', default=50),
)

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Stethoscope API Documentation',
    'DESCRIPTION': 'Stethoscope API Documentation description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'TOS': 'https://stethoscope.acceleratorpracticum.ru/terms/',
    'CONTACT': {'email': 'info@stethoscope.acceleratorpracticum.ru'},
    'LICENSE': {'name': 'BSD License'},
}

SITE_NAME = os.environ.get('SITE_NAME')
DOMAIN = os.environ.get('DOMAIN')
PASSWORD_RESET_TIMEOUT = int(os.environ.get('PASSWORD_RESET_TIMEOUT', 259200))

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'reset-password-confirmation/?uid={uid}&token={token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'EMAIL': {
        'activation': 'core.email_djoser.ActivationEmail',
        'confirmation': 'core.email_djoser.ConfirmationEmail',
        'password_reset': 'core.email_djoser.PasswordResetEmail',
        'password_changed_confirmation': 'core.email_djoser.PasswordConfirmationEmail',
    },
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'ACTIVATION_URL': 'activate/?uid={uid}&token={token}',
    'SEND_ACTIVATION_EMAIL': True,
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'activation': 'api.serializers.ActivationSerializer',
        'user': 'api.serializers.UserSerializer',
        'current_user': 'api.serializers.UserSerializer',
    },
    'HIDE_USERS': True,
    'CONSTANTS': {
        'messages': 'api.constants.DjoserMessages',
    },
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', default='False').lower() == 'true'
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', default='False').lower() == 'true'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = ['locale']

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING_ENABLED = os.environ.get('LOGGING_ENABLED', 'False') == 'True'

if LOGGING_ENABLED:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER', 'redis://localhost:6379/0')
WEEKLY_SUBJECT = os.environ.get('WEEKLY_SUBJECT', 'Еженедельная рассылка Стетоскоп')
URL_ARTICLES = os.environ.get('URL_ARTICLES', 'http://localhost:8000/articles/')

# https://github.com/pylixm/django-mdeditor#customize-the-toolbar
MDEDITOR_CONFIGS = {
    'default': {
        'width': '100%',  # Custom edit box width
        'height': 400,  # Custom edit box height
        'toolbar': [
            'undo',
            'redo',
            '|',
            'bold',
            'del',
            'italic',
            'quote',
            'uppercase',
            'lowercase',
            '|',
            'h1',
            'h2',
            'h3',
            'h5',
            'h6',
            '|',
            'list-ul',
            'list-ol',
            'hr',
            '|',
            'link',
            'reference-link',
            'table',
            'emoji',
            '|',
            'preview',
            'watch',
            'fullscreen',
        ],  # custom edit box toolbar
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'watch': False,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False,  # lineNumbers
        'language': 'en',  # zh / en / es
    },
}

# non-activated user account management settings
TIME_TO_ACTIVATE_USER_ACCOUNT = timedelta(minutes=10)
USER_NON_ACTIVATED_ACCOUNT_CLEANUP_PERIOD = timedelta(hours=1)


# BASE64 ENCODED IMAGE SERIALIZATION SETTINGS
ALLOWED_B64ENCODED_IMAGE_FORMATS = ('jpg', 'jpeg', 'png')
BASE64_IMAGE_MAX_SIZE_BYTES = 1_500_000
BASE64_AVATAR_MAX_SIZE_BYTES = 200_000
BASE64_AVATAR_MAX_WIDTH = 500
BASE64_AVATAR_MAX_HEIGHT = 500
