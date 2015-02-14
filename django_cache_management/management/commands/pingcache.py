from django.core.management.base import BaseCommand, CommandError
from django.core.cache import get_cache
from django.conf import settings

from optparse import make_option

class Command(BaseCommand):
    help = """
Ping one or more caches.
    """
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
