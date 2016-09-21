This is a Django application that adds management commands for
managing your caches.

It has been tested with these combinations:

- Python 2.7 and 3.4, and Django 1.7,

- Python 2.7, 3.4 and 3.5 and Django 1.8, 1.9, 1.10.

This code is currently used in production.

It provides these commands:

* ``listcaches``: lists the caches configured in your Django project.

* ``pingcache``: verifies that one or more caches are accessible
  ("pings" them).

* ``clearcache``: clears one or more caches.

### Changelog

* 1.0.1:

  + Added formal support for Django 1.9, 1.10. The previous version
    was already running fine on them, but the dependencies and the
    test setup have been tweaked for these versions of Django.

  + Drop support for Django 1.6.
