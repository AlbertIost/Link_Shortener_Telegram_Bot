from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_shortener_link_tgbot',
        'USER': 'admin',
        'PASSWORD': 'pass1234',
        'HOST': 'db',
        'PORT': '3306',
    }
}