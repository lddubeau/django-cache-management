import json
import re

from django.core.management.base import BaseCommand
from django.conf import settings

# json.dumps adds unnecessary white space before newlines. We use this
# regex to clean them.
clean_re = re.compile(r" +\n")

UNSERIALIZABLE = "***UNSERIALIZABLE VALUE***"

class Command(BaseCommand):

    """
    Lists the caches defined in your project's settings.

    Note that this command is meant to provide a quick "lay of the
    land" and is not a substitute for reading your settings. This
    command dumps the configurations it finds using
    ``json.dumps``. Values that cannot be serialized will be shown as
    "***UNSERIALIZABLE VALUE***"

    .. warning:: This may expose SENSITIVE INFORMATION, like
    passwords.
    """

    help = __doc__

    def handle(self, *args, **options):
        for name, value in sorted(settings.CACHES.items()):
            self.stdout.write("Cache named: " + name)
            # We use dumps to pretty-print the dictionary
            self.stdout.write(
                clean_re.sub(u"\n",
                             json.dumps(value, indent=4,
                                        default=lambda *_: UNSERIALIZABLE)))
            self.stdout.write("")
