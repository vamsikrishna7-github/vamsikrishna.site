"""
Django settings for vamsikrishna project.
"""

from pathlib import Path
import os
from corsheaders.defaults import default_headers
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary Config (Image Storage)
cloudinary.config( 
  cloud_name = "djzsfnsjj",  
  api_key = "489235114815498",  
  api_secret = "HKC-xb3NsenxGSB4ChZSidi7J9c"  
)

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = 'django-insecure-#6p#pz(%pk68(3lg1+^hh90&ro8x*eazi7upof5n@!4v)ii0(t'
DEBUG = False  # Set to True for development

ALLOWED_HOSTS = [
    "vamsikrishna.site",
    "www.vamsikrishna.site",
    "blog.vamsikrishna.site",
    "www.blog.vamsikrishna.site",
    "vamsikrishna-site.onrender.com",  # Render backend
    "vamsi-blog.vercel.app",  # Vercel frontend
    "127.0.0.1",
    "localhost:8000",
]

# ✅ CORS Settings (Fix CORS Issues)
CORS_ALLOW_ALL_ORIGINS = False  # Security: Don't allow all origins
CORS_ALLOWED_ORIGINS = [
    "https://blog.vamsikrishna.site",
    "https://www.blog.vamsikrishna.site",
    "https://vamsikrishna.site",
    "https://www.vamsikrishna.site",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:8000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = list(default_headers) + ["content-disposition"]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS  # Allow trusted origins for CSRF

# ✅ Redirect HTTP to HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False
# Application Definition
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home",
    "captcha",
    "django_recaptcha",
    "cloudinary",
    "cloudinary_storage",
    "blog",
    "rest_framework",
    "social_django",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vamsikrishna.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "vamsikrishna.wsgi.application"

# ✅ Database Configuration (PostgreSQL on Render)
DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://neondb_owner:npg_mfeMUXr40blK@ep-raspy-shape-a5ktfyv6-pooler.us-east-2.aws.neon.tech/vamsikrishna_site?sslmode=require",
        conn_max_age=600
    )
}


# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localization Settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files (Cloudinary for Media)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
MEDIA_URL = "https://res.cloudinary.com/djzsfnsjj/"

# Development static files serving
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    WHITENOISE_MANIFEST_STRICT = False
    WHITENOISE_ALLOW_ALL_ORIGINS = True

# Admin Panel Login
LOGIN_URL = "/admin/"

# ✅ Email Configuration (Zoho Mail)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.zoho.in"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "contact@vamsikrishna.site"
EMAIL_HOST_PASSWORD = "MKVEca9WUERn"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ✅ reCAPTCHA Settings
if DEBUG:
    RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
else:
    RECAPTCHA_PUBLIC_KEY = "6Lds4e0qAAAAAMo-hNW5n7ViSl29D6vZBmGJPKGj"
    RECAPTCHA_PRIVATE_KEY = "6Lds4e0qAAAAAEU5awIdxjQz1bPVZ80RBfe1PZnD"

RECAPTCHA_REQUIRED = True

#Razerpay
RAZORPAY_KEY_ID = 'rzp_live_JYd4C2kFByLggN'
RAZORPAY_KEY_SECRET = 'ShybyuTubacF63AhJfvUGSV3'


#login with google
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '245460647363-mvqdqlj00lsp70ac1g7glab0056mg3d3.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

LOGIN_REDIRECT_URL = 'admin_panel'
LOGOUT_REDIRECT_URL = 'admin'

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'social_django.context_processors.backends',
    'social_django.context_processors.login_redirect',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'home.pipeline.validate_admin_email',  # ✅ Your custom step
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
