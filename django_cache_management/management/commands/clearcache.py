from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.cache import caches

class Command(BaseCommand):

    """
Clear one or more caches.

Note that the clear operation is not guaranteed to be atomic.
    """
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument("cache_names", nargs="*")
        parser.add_argument('--noop',
                            action='store_true',
                            dest='noop',
                            default=False,
                            help='Do not actually perform the action.')
        parser.add_argument('--all',
                            action='store_true',
                            dest='all',
                            default=False,
                            help='Clear all caches.')
        parser.add_argument('--method',
                            dest='method',
                            default="conservative",
                            choices=("conservative", "django-clear"),
                            help="""
The method to use. The method "conservative" will remove only the
keys that begin with the cache's prefix. The method "django-clear"
will use Django's ``clear`` method, which will delete even keys that are
not prefixed with the cache's key. "conservative" is the default.
""".strip())

    def handle(self, *args, **options):
        cache_names = options["cache_names"]
        if options["all"]:
            if cache_names:
                raise CommandError("cannot use --all with a cache name")

            cache_names = settings.CACHES.keys()
        else:
            if not cache_names:
                raise CommandError("specify at least one cache to clear")

            # Make sure all names given exist
            for name in cache_names:
                caches[name]

        method = options["method"]
        noop = options["noop"]

        action = "Clearing " if not noop else "Not clearing "

        if method == "conservative":
            for name in cache_names:
                config = settings.CACHES[name]
                backend = config["BACKEND"]
                failed = False
                if backend.startswith("django_redis."):
                    try:
                        import django_redis
                        django_redis.get_redis_connection(name)
                        # Yes, we grab all exceptions. It is up to the
                        # user to diagnose how their configuration is
                        # wrong.
                    except:  # pylint: disable=bare-except
                        failed = True
                else:
                    failed = True

                if failed:
                    raise CommandError(
                        "clearcache does not know how to "
                        "conservatively clear a "
                        "cache with backend {0}".format(backend))

            for name in cache_names:
                self.stdout.write(action + name)
                config = settings.CACHES[name]
                cache = caches[name]
                prefix = cache.key_prefix
                backend = config["BACKEND"]
                if backend.startswith("django_redis."):
                    import django_redis
                    con = django_redis.get_redis_connection(name)
                    keys = con.keys(prefix + ':*')
                    if keys and not noop:
                        con.delete(*keys)
        else:
            for name in cache_names:
                self.stdout.write(action + name)
                cache = caches[name]
                if not noop:
                    cache.clear()
