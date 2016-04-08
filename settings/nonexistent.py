from .normal import *

CACHES['nonexistent'] = {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'unix:///dev/null',
    'KEY_PREFIX': 'foo',
    'OPTIONS': {
        "CLIENT_CLASS": "django_redis.client.DefaultClient"
    }
}
