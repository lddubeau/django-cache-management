from subprocess import Popen, PIPE
import unittest
import os
import time

import six
from django.test.utils import override_settings
from django.test.testcases import SimpleTestCase
from nose.tools import assert_equal

from settings import clearcache

# We set ``using_caches`` because our software merely lets the exceptions
# caused by referencing bad cache names trickle up, and these
# exceptions are different depending on whether ``caches`` is used or
# ``get_cache``.
try:
    # Django 1.7 and later
    from django.core.cache import caches

    def get_cache(name):
        return caches[name]

    def make_expected_missing_cache_error(name):
        return \
            ("django.core.cache.backends.base.InvalidCacheBackendError: "
             "Could not find config for \'{0}\' in settings.CACHES") \
            .format(name).encode()

    using_caches = True
except ImportError:
    # Django 1.6
    from django.core.cache import get_cache
    using_caches = False

    def make_expected_missing_cache_error(name):
        return \
            ("django.core.cache.backends.base.InvalidCacheBackendError: "
             "Could not find backend \'{0}\'").format(name).encode()

CWD = os.getcwd()

def test_listcaches():
    p = Popen(["./manage.py", "listcaches"], stdout=PIPE, stderr=PIPE)
    (out, err) = p.communicate()
    expected = b"""\
Cache named: default
{
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
}

Cache named: foo
{
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
}

"""
    assert_equal(err, b"", "stderr should be empty")
    assert_equal(out, expected, "stdout should be a list of caches"
                 " and their settings")

class ExecMixin(object):
    command = None

    def manage(self, args):
        p = Popen(["./manage.py"] + args, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        return (out, err, p)

    def runcmd(self, args):
        return self.manage([self.command] + args)

class PingTestCase(unittest.TestCase, ExecMixin):

    command = "pingcache"

    def test_pingcache_all_successful(self):
        (out, err, p) = self.runcmd(["--all"])
        self.assertEqual(out, b"""\
Pinging default... successful
Pinging foo... successful
""")
        self.assertEqual(err, b"")
        self.assertEqual(p.returncode, 0)

    def test_pingcache_all_fails(self):
        (out, err, p) = self.runcmd(["--all",
                                     "--settings=settings.nonexistent"])
        self.assertEqual(out, b"""\
Pinging default... successful
Pinging foo... successful
Pinging nonexistent... unsuccessful
""")
        self.assertEqual(err, b"CommandError: ping failed\n")
        self.assertEqual(p.returncode, 1)

    def test_pingcache_some_successful(self):
        (out, err, p) = self.runcmd(["default", "foo",
                                     "--settings=settings.nonexistent"])
        self.assertEqual(out, b"""\
Pinging default... successful
Pinging foo... successful
""")
        self.assertEqual(err, b"")
        self.assertEqual(p.returncode, 0)

    def test_pingcache_unknown_cache(self):
        (out, err, p) = self.runcmd(["blah"])
        self.assertEqual(out, b"")
        six.assertRegex(self,
                        err,
                        make_expected_missing_cache_error("blah"))

        self.assertEqual(p.returncode, 1)

    def test_pingcache_no_cache(self):
        (out, err, p) = self.runcmd([])
        self.assertEqual(out, b"")
        self.assertEqual(
            err, b"CommandError: specify at least one cache to ping\n")
        self.assertEqual(p.returncode, 1)

@override_settings(CACHES=clearcache.CACHES)
class ClearcacheTestCase(SimpleTestCase, ExecMixin):

    command = "clearcache"

    def setUp(self):
        super(ClearcacheTestCase, self).setUp()
        self.redis = Popen(["redis-server", "./redis.conf"])
        while not os.path.exists("./var/redis.sock"):
            time.sleep(0.1)

    def tearDown(self):
        super(ClearcacheTestCase, self).tearDown()
        self.redis.terminate()
        self.redis.wait()

    def test_clearcache_no_cache(self):
        (out, err, p) = self.runcmd([])
        self.assertEqual(out, b"")
        self.assertEqual(
            err, b"CommandError: specify at least one cache to clear\n")
        self.assertEqual(p.returncode, 1)

    def test_pingcache_unknown_cache(self):
        (out, err, p) = self.runcmd(["blah"])
        self.assertEqual(out, b"")
        six.assertRegex(self,
                        err,
                        make_expected_missing_cache_error("blah"))
        self.assertEqual(p.returncode, 1)

    def test_clearcache_conservative_clears_only_one_cache(self, explicit=False):
        redis1 = get_cache('redis1')
        redis1.set('foo', 'foo value 1')

        redis2 = get_cache('redis2')
        redis2.set('foo', 'foo value 2')

        self.assertEqual(redis1.get('foo'), 'foo value 1')
        self.assertEqual(redis2.get('foo'), 'foo value 2')

        cmd = ['redis1', '--settings=settings.clearcache']
        if explicit:
            cmd.append("--method=conservative")

        (out, err, p) = self.runcmd(cmd)
        self.assertEqual(out, b'Clearing redis1\n')
        self.assertEqual(err, b'')
        self.assertEqual(p.returncode, 0)

        self.assertIsNone(redis1.get('foo'))
        self.assertEqual(redis2.get('foo'), 'foo value 2')

    def test_clearcache_explicit_conservative_clears_only_one_cache(self):
        self.test_clearcache_conservative_clears_only_one_cache(True)

    def test_clearcache_django_clear_clears_everything(self):
        redis1 = get_cache('redis1')
        redis1.set('foo', 'foo value 1')

        redis2 = get_cache('redis2')
        redis2.set('foo', 'foo value 2')

        self.assertEqual(redis1.get('foo'), 'foo value 1')
        self.assertEqual(redis2.get('foo'), 'foo value 2')

        (out, err, p) = self.runcmd(['redis1',
                                     '--method=django-clear',
                                     '--settings=settings.clearcache'])
        self.assertEqual(out, b'Clearing redis1\n')
        self.assertEqual(err, b'')
        self.assertEqual(p.returncode, 0)

        self.assertIsNone(redis1.get('foo'))
        #
        # We cannot run this test until this is fixed:
        #
        # https://github.com/niwinz/django-redis/issues/223
        # self.assertIsNone(redis2.get('foo'))
