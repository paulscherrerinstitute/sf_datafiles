#!/usr/bin/env python

from utils import TestCase

from sfdata.sfmeta import SFMeta


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



