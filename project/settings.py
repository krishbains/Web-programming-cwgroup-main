from . import database
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    # safe value used for development when DJANGO_SECRET_KEY might not be set
    'django-insecure-8^fq+a!kh-4pm8#y(urc^&zum$01nvb69$s=vnif(#gn6o7)_!'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Moved whitenoise to top
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add OpenShift URL to CORS if we're in OpenShift
if os.getenv('OPENSHIFT_BUILD_NAME'):
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "https://django-psql-persistent-web-apps-ec22663.apps.a.comp-teach.qmul.ac.uk",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
    ]

CSRF_TRUSTED_ORIGINS = [
    "https://django-psql-persistent-web-apps-ec22663.apps.a.comp-teach.qmul.ac.uk",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database configuration
DATABASES = {
    'default': database.config()
}

# Add test database configuration
if os.getenv('OPENSHIFT_BUILD_NAME'):
    DATABASES['default']['TEST'] = {
        'NAME': os.getenv('DATABASE_NAME', 'django'),
    }

AUTH_USER_MODEL = 'api.CustomUser'
TIME_ZONE = 'Europe/London'
# Rest of your settings remain the same...
# Password validation, Internationalization, Static files, etc.

# Static files configuration for OpenShift
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Only include internal IPs in development
if not os.getenv('OPENSHIFT_BUILD_NAME'):
    INTERNAL_IPS = ['127.0.0.1']