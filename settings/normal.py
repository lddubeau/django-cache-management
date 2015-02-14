import os

CWD = os.getcwd()

REDIS_LOCATION = 'unix://{0}/var/redis.sock?db=0'.format(CWD)

SECRET_KEY = "whatever"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django_cache_management',
    'django_nose'
)

CACHES = {
    'default': {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    },
    'foo': {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MIDDLEWARE_CLASSES = ()
