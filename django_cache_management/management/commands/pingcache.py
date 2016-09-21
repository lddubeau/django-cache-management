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
Ping one or more caches. This is done by performing a non-destructive
access of the cache through Django's cache framework. Some cache
backends can be configured to hide accessibility problems
(e.g. ``django_redis`` with the ``IGNORE_EXCEPTIONS`` turned on). In
such cases, this command will report that the cache is accessible (the
ping will succeed) even if it may not be in fact accessible.
    """
    help = __doc__

    args = "[cache_name ...]"

    option_list = BaseCommand.option_list + (
        make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False,
                    help='Ping all caches.'),
    )

    def handle(self, *args, **options):
        if options["all"]:
            if args:
                raise CommandError("cannot use --all with a cache name")

            args = sorted(settings.CACHES.keys())
        else:
            if not args:
                raise CommandError("specify at least one cache to ping")

            # Make sure all names given exist
            for name in args:
                get_cache(name)

        failed = False
        for name in args:
            cache = get_cache(name)
            try:
                "foo" in cache
            except:  # pylint: disable=bare-except
                result = "... unsuccessful"
                failed = True
            else:
                result = "... successful"
            self.stdout.write("Pinging " + name + result)

        if failed:
            raise CommandError("ping failed")
