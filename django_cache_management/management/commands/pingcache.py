from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.cache import caches

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

    def add_arguments(self, parser):
        parser.add_argument("cache_names", nargs="*")
        parser.add_argument("--all",
                            action="store_true",
                            dest="all",
                            default=False,
                            help="Ping all caches.")

    def handle(self, *args, **options):
        cache_names = options["cache_names"]
        if options["all"]:
            if cache_names:
                raise CommandError("cannot use --all with a cache name")

            cache_names = sorted(settings.CACHES.keys())
        else:
            if not cache_names:
                raise CommandError("specify at least one cache to ping")

            # Make sure all names given exist
            for name in cache_names:
                caches[name]

        failed = False
        for name in cache_names:
            cache = caches[name]
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
