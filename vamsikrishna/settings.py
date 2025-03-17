from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep this secret in production
SECRET_KEY = 'django-insecure-#6p#pz(%pk68(3lg1+^hh90&ro8x*eazi7upof5n@!4v)ii0(t'

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = True  # Keep as per your requirement

# Allowed hosts
ALLOWED_HOSTS = ['vamsikrishna.site', 'www.vamsikrishna.site', '13.234.51.218', 'localhost', '127.0.0.1']

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://vamsikrishna.site",
    "http://vamsikrishna.site"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'captcha',
    'django_recaptcha',
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

ROOT_URLCONF = 'vamsikrishna.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'vamsikrishna.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin Login URL
LOGIN_URL = '/admin/'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.in'  # Zoho India SMTP
EMAIL_PORT = 587  # Use 465 if using SSL
EMAIL_USE_TLS = True  # Set to False if using SSL
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'contact@vamsikrishna.site'  # Your Zoho email
EMAIL_HOST_PASSWORD = 'MKVEca9WUERn'  # Your Zoho App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default sender email

# Google reCAPTCHA Keys
RECAPTCHA_PUBLIC_KEY = "6Lds4e0qAAAAAMo-hNW5n7ViSl29D6vZBmGJPKGj"
RECAPTCHA_PRIVATE_KEY = "6Lds4e0qAAAAAEU5awIdxjQz1bPVZ80RBfe1PZnD"
RECAPTCHA_REQUIRED = True

# Silence system check warnings (optional)
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

# Optimize static file storage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
