#!/usr/bin/env python

import unittest.mock

from utils import TestCase

from sfdata.sfdatafile import FileDemultiplexer


class TestFileDemultiplexer(TestCase):

    def test_closed(self):
        mopen = unittest.mock.mock_open()

        fnames = ["f{i}" for i in range(5)]
        fs = [mopen(fn) for fn in fnames]

        fdemux = FileDemultiplexer(fs)

        for f in fs:
            f.close.assert_not_called()

        fdemux.close()

        for f in fs:
            f.close.assert_called_once()



