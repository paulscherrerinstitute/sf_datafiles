#!/usr/bin/env python

from utils import TestCase

from sfdata.sfmeta import SFMeta, get_meta


class TestSFMeta(TestCase):

    def run(self, *args, **kwargs):
        self.orig = d = {
            "a": [0, 1],
            "b": [1, 2, 3]
        }
        self.meta = SFMeta(d)
        super().run(*args, **kwargs)


    def test_names(self):
        self.assertEqual(
            self.meta.names, self.meta.keys()
        )
        self.assertEqual(
            self.meta.names, self.orig.keys()
        )

    def test_getitem(self):
        for k, v in self.orig.items():
            self.assertEqual(
                self.meta[k], v
            )

    def test_getitem_missing(self):
        with self.assertRaises(KeyError):
            self.meta["notakey"]

    def test_repr(self):
        self.assertEqual(
            repr(self.meta), "SFMeta: 2 entries"
        )


    def test_get_meta(self):
        res = {"test": 123}
        group = {"meta": res}
        self.assertEqual(
            get_meta(group), res
        )

    def test_get_meta_missing(self):
        group = {}
        self.assertEqual(
            get_meta(group), None
        )


    def test_cache(self):
        m = SFMeta(self.orig)
        self.helper_test_meta_cache(m)

    def test_cache_test_helper(self):
        m = SFMeta(self.orig)
        self.helper_test_meta_cache(m)
        # should fail on the second run
        with self.assertRaises(AssertionError):
            self.helper_test_meta_cache(m)

    def test_cache_reset_with_clear(self):
        m = SFMeta(self.orig)
        self.helper_test_meta_cache(m)
        m._getitem.cache_clear()
        self.helper_test_meta_cache(m)

    def test_cache_reset_with_close(self):
        m = SFMeta(self.orig)
        self.helper_test_meta_cache(m)
        m.close()
        self.helper_test_meta_cache(m)

    def test_caches_independent(self):
        m1 = SFMeta(self.orig)
        m2 = SFMeta(self.orig)
        self.helper_test_meta_cache(m1)
        self.helper_test_meta_cache(m2)

    def test_caches_independent_with_clear(self):
        m1 = SFMeta(self.orig)
        m2 = SFMeta(self.orig)
        self.helper_test_meta_cache(m1)
        m1._getitem.cache_clear()
        self.helper_test_meta_cache(m2)

    def test_caches_independent_with_close(self):
        m1 = SFMeta(self.orig)
        m2 = SFMeta(self.orig)
        self.helper_test_meta_cache(m1)
        m1.close()
        self.helper_test_meta_cache(m2)

    def helper_test_meta_cache(self, m):
        ci = m._getitem.cache_info()
        self.assertEqual(ci.hits, 0)
        self.assertEqual(ci.misses, 0)
        self.assertEqual(ci.currsize, 0)
        m["a"]
        ci = m._getitem.cache_info()
        self.assertEqual(ci.hits, 0)
        self.assertEqual(ci.misses, 1)
        self.assertEqual(ci.currsize, 1)
        m["a"]
        ci = m._getitem.cache_info()
        self.assertEqual(ci.hits, 1)
        self.assertEqual(ci.misses, 1)
        self.assertEqual(ci.currsize, 1)
        m["a"]
        ci = m._getitem.cache_info()
        self.assertEqual(ci.hits, 2)
        self.assertEqual(ci.misses, 1)
        self.assertEqual(ci.currsize, 1)
        m["b"]
        ci = m._getitem.cache_info()
        self.assertEqual(ci.hits, 2)
        self.assertEqual(ci.misses, 2)
        self.assertEqual(ci.currsize, 2)
        m["b"]
        ci = m._getitem.cache_info()
        self.assertEqual(ci.hits, 3)
        self.assertEqual(ci.misses, 2)
        self.assertEqual(ci.currsize, 2)



