#!/usr/bin/env python

import sys
import os

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.normal")

from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
