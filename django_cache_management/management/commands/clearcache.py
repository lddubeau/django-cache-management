from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from optparse import make_option

try:
    # Django 1.7 and later
    from django.core.cache import caches

    def get_cache(name):
        return caches[name]
except ImportError:
    # Django 1.6
    from django.core.cache import get_cache


class Command(BaseCommand):

    """
Clear one or more cache.

Note that the clear operation is not guaranteed to be atomic.
    """
    help = __doc__

    args = "[cache_name ...]"

    option_list = BaseCommand.option_list + (
        make_option('--noop',
                    action='store_true',
                    dest='noop',
                    default=False,
                    help='Do not actually perform the action.'),
        make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False,
                    help='Clear all caches.'),
        make_option('--method',
                    dest='method',
                    default="conservative",
                    choices=("conservative", "django-clear"),
                    help="""
The method to use. The method "conservative" will remove only the
keys that begin with the cache's prefix. The method "django-clear"
will use Django's ``clear`` method, which will delete even keys that are
not prefixed with the cache's key. "conservative" is the default.
""".strip()),
    )

    def handle(self, *args, **options):
        if options["all"]:
            if args:
                raise CommandError("cannot use --all with a cache name")

            args = settings.CACHES.keys()
        else:
            if not args:
                raise CommandError("specify at least one cache to clear")

            # Make sure all names given exist
            for name in args:
                get_cache(name)

        method = options["method"]
        noop = options["noop"]

        action = "Clearing " if not noop else "Not clearing "

        if method == "conservative":
            for name in args:
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

            for name in args:
                self.stdout.write(action + name)
                config = settings.CACHES[name]
                cache = get_cache(name)
                prefix = cache.key_prefix
                backend = config["BACKEND"]
                if backend.startswith("django_redis."):
                    import django_redis
                    con = django_redis.get_redis_connection(name)
                    keys = con.keys(prefix + ':*')
                    if keys and not noop:
                        con.delete(*keys)
        else:
            for name in args:
                self.stdout.write(action + name)
                cache = get_cache(name)
                if not noop:
                    cache.clear()
