This is a Django application that adds management commands for
managing your caches.

It has been tested with these combinations:

- Python 3.6, 3.7, 3.8 and Django 2.2, 3.0, 3.1.

This code is currently used in production.

It provides these commands:

* ``listcaches``: lists the caches configured in your Django project.

* ``pingcache``: verifies that one or more caches are accessible
  ("pings" them).

* ``clearcache``: clears one or more caches.

### Changelog

* 5.0.0:

  + Fix setup.py to avoid packaging the folders that pertain only to
    development.

  + Drop support for Django 1.1. It reached EOL.

  + Drop support for Python 3.5. We're two weeks away from its EOL.

  + Formally test on Python 3.6 and 3.8.

  + Formally test on Django 3.0 and 3.1. (It was already compatible but now tox
    run tests on these versions.)

* 4.0.1:

  + Don't use or require ``six`` anymore. It was an oversight that it stayed in
    after we dropped support for Python 2.7.

* 4.0.0:

  + Formally support Django 2.2. (This package already worked fine on it.)

  + Drop support for Django 2.0. It reached EOL.

  + Drop support for Python 2.7 and 3.4.

* 3.0.0:

  + Drop support for Django versions prior to 1.11. This is a breaking change
    and so require a new major number.

  + Formally support 1.11, 2.0 and 2.1. (This package already worked fine on
    them.)

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
