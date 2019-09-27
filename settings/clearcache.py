from .normal import *

for index in range(1, 3):
    name = 'redis' + str(index)
    CACHES[name] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'KEY_PREFIX': name + '!',
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
