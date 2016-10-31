This is a Django application that adds management commands for
managing your caches.

It has been tested with these combinations:

- Python 2.7, 3.4 and 3.5 and Django 1.8, 1.9, 1.10.

This code is currently used in production.

It provides these commands:

* ``listcaches``: lists the caches configured in your Django project.

* ``pingcache``: verifies that one or more caches are accessible
  ("pings" them).

* ``clearcache``: clears one or more caches.

### Changelog

* 2.0.0:

  + Formally follow the semver spec for version numbers. Previous
    version numbers were bumped haphazardly.

  + Drop support for Django 1.7.

  + Fix problems with running on Django 1.10. Version 1.0.1 was
    supposed to support Django 1.10 but I discovered, much to my
    displeasure, that ``tox`` silently disregarded the disconnect
    between its test specification ("please install Django 1.10.x")
    and a mistake in ``setup.py`` ("I want a Django version lower than
    1.10"). The net result was that the tests that were supposed to be
    done with 1.10 were done with a lower version... *sigh*.

  + ``listcaches`` now supports the case where the configuration
    settings for caches contain unserializable values.

* 1.0.1:

  + Added formal support for Django 1.9, 1.10. The previous version
    was already running fine on them, but the dependencies and the
    test setup have been tweaked for these versions of Django.

  + Drop support for Django 1.6.
