
from pathlib import Path
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-yf*mw+zoxc1exq@%0uba(=a#ao-!e@_0^4+0*%slc@&j(du9qu'


DEBUG = False

ALLOWED_HOSTS = ["*"]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Mainapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MilkConnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "Mainapp" / "templates"],
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

WSGI_APPLICATION = 'MilkConnect.wsgi.application'


# Database


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'milk_connect',
        'USER': 'milk_connect_user',
        'PASSWORD': 'XOGGnEtwXRb6Gymgq9luQaASrL7PvLVl',
        'HOST': 'dpg-d2kk4mbuibrs73e9bqc0-a.oregon-postgres.render.com',  # external hostname
        'PORT': '5432',
    }
}




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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"



STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
cloudinary.config( 
  cloud_name = "dsanolt1o", 
  api_key = "258941222218578", 
  api_secret = "oo5Vi-3PKzG2OpdsZYihHT6DOko",  # Replace with your real secret
  secure = True
)


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pal0552609@gmail.com'  
EMAIL_HOST_PASSWORD = 'kcaq rcdm fdlp tqyx' 


RAZORPAY_KEY_ID = "rzp_test_kJFCr5jnzPYy9s"
RAZORPAY_KEY_SECRET = "cFR0T4bhyI16Xb06fFytJmAu"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
