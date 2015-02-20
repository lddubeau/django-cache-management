Welcome to django-cache-management's documentation!
===================================================

This is a Django application that adds management commands for
managing your caches.

It provides these commands:

* ``listcaches [names...]``

  Lists the caches specified as arguments to the command.

  .. warning:: This may expose SENSITIVE INFORMATION, like
               passwords.

  Options:

  - ``--all``: List all the caches. Do not pass names when using this
    option.

* ``pingcache [names...]``

  Verifies that one or more caches are accessible ("pings" them).

  Options:

  - ``--all``: Ping all the caches. Do not pass names when using this
    option.

* ``clearcache [names...]``

  Clears one or more caches.

  - ``--noop``: Do not actually perform the action. You can use this
    to test the arguments you are passing to the command.

  - ``--all``: Clear all the caches. Do not pass names when using this
    option.

  - ``--method=..``: The method to use to clear the cache.

    + ``conservative``: Remove only the keys that begin with the
      cache's prefix. This is the default.

    + ``django-clear``: Use Django's ``clear`` method, which will
      delete even keys that are not prefixed with the cache's
      key.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
