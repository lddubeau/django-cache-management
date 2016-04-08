This is a Django application that adds management commands for
managing your caches.

It has been tested with these combinations:

- Python 2.7 and 3.4, and Django 1.6 and 1.7,

- Python 2.7, 3.4 and 3.5 and Django 1.8 and 1.9.

This code is currently used in production.

It provides these commands:

* ``listcaches``: lists the caches configured in your Django project.

* ``pingcache``: verifies that one or more caches are accessible
  ("pings" them).

* ``clearcache``: clears one or more caches.
