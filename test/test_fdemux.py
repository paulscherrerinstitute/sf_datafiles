#!/usr/bin/env python

import unittest.mock

from utils import TestCase

from sfdata.utils import FileDemultiplexer


def mopen(*args, **kwargs):
    mo = unittest.mock.mock_open()
    return mo(*args, **kwargs)


class TestFileDemultiplexer(TestCase):

    def test_closed(self):
        fnames = ["f{i}" for i in range(5)]
        fs = [mopen(fn) for fn in fnames]

        subs = mopen("subs")

        fdemux = FileDemultiplexer(fs, substitute=subs)

        for f in fs:
            f.close.assert_not_called()

        fdemux.substitute.close.assert_not_called()

        fdemux.close()

        for f in fs:
            f.close.assert_called_once()

        fdemux.substitute.close.assert_called_once()


    def test_substitute(self):
        n = "substitue_entry"
        subs = {n: 123}
        fdemux = FileDemultiplexer(substitute=subs)
        self.assertEqual(
            fdemux[n], subs[n]
        )


    def test_no_substitute(self):
        fdemux = FileDemultiplexer(substitute=None)
        with self.assertRaises(ValueError):
            fdemux["substitue_entry"]



