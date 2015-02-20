import json
import re

import six
from django.core.management.base import BaseCommand
from django.conf import settings

# json.dumps adds unnecessary white space before newlines. We use this
# regex to clean them.
clean_re = re.compile(r" +\n")

class Command(BaseCommand):

    """
    Lists the caches defined in your project's settings.

    .. warning:: This may expose SENSITIVE INFORMATION, like
    passwords.
    """

    help = __doc__

    def handle(self, *args, **options):
        for name, value in sorted(six.iteritems(settings.CACHES)):
            self.stdout.write("Cache named: " + name)
            # We use dumps to pretty-print the dictionary
            self.stdout.write(clean_re.sub(u"\n",
                                           json.dumps(value, indent=4)))
            self.stdout.write("")
