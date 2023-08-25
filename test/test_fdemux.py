#!/usr/bin/env python

import unittest.mock

from utils import TestCase

from sfdata.utils import FileDemultiplexer


def mopen(*args, **kwargs):
    mo = unittest.mock.mock_open()
    return mo(*args, **kwargs)



class TestFileDemultiplexer(TestCase):

    def test_closed(self):
        fs, sub = mk_demux_args()

        fdemux = FileDemultiplexer(fs, substitute=sub)

        for f in fs:
            f.close.assert_not_called()

        sub.close.assert_not_called()

        fdemux.close()

        for f in fs:
            f.close.assert_called_once()

        sub.close.assert_called_once()


    def test_substitute(self):
        n = "substitute_entry"
        sub = {n: 123}
        fdemux = FileDemultiplexer(substitute=sub)
        self.assertEqual(
            fdemux[n], sub[n]
        )


    def test_no_substitute(self):
        fdemux = FileDemultiplexer(substitute=None)
        with self.assertRaises(ValueError):
            fdemux["substitute_entry"]


    def test_repr_name(self):
        fs, sub = mk_demux_args()

        fdemux = FileDemultiplexer(fs, substitute=sub, name="test_name")

        ref = '<FileDemultiplexer "test_name" (5 instances)>'

        self.assertEqual(
            repr(fdemux), ref
        )


    def test_repr_no_name(self):
        fs, sub = mk_demux_args()

        fdemux = FileDemultiplexer(fs, substitute=sub, name=None)

        ref = '<Unnamed FileDemultiplexer (5 instances)>'

        self.assertEqual(
            repr(fdemux), ref
        )



def mk_demux_args():
    fnames = ["f{i}" for i in range(5)]
    fs = [mopen(fn) for fn in fnames]
    sub = mopen("sub")
    return fs, sub



