This is a Django application that adds management commands for
managing your caches.

It has been tested with Python 2.7 and Python 3.4, and with Django
1.6, 1.7 and 1.8. This code is currently used in production.

It provides these commands:

* ``listcaches``: lists the caches configured in your Django project.

* ``pingcache``: verifies that one or more caches are accessible
  ("pings" them).

* ``clearcache``: clears one or more caches.
