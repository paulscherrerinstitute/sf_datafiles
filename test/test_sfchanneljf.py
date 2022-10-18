#!/usr/bin/env python

import unittest.mock

from utils import TestCase

import sfdata
from sfdata import SFDataFile


class TestSFChannelJF(TestCase):

    det_name = "JFxxx"
    fname = f"fake_data/run_testjf.{det_name}.h5"

    @unittest.mock.patch("jungfrau_utils.File")
    def test_create(self, _):
        with SFDataFile(self.fname) as data:
            pass

    @unittest.mock.patch("jungfrau_utils.File.detector_name", det_name)
    @unittest.mock.patch("jungfrau_utils.file_adapter.JFDataHandler")
    @unittest.mock.patch("jungfrau_utils.file_adapter.locate_gain_file", lambda path: "fn_gain")
    @unittest.mock.patch("jungfrau_utils.file_adapter.locate_pedestal_file", lambda path: "fn_pedestal")
    def test_shape(self, _):
        with SFDataFile(self.fname) as data:
            ch = data[self.det_name]
            self.assertEqual(
                ch.shape, (3,)
            )
            self.assertAllEqual(
                ch.pids, [0, 1, 2]
            )


    @unittest.mock.patch("sfdata.sfdatafile.ju", None)
    def test_no_ju(self):
        modfname = sfdata.sfdatafile.__file__
        line = 24 #TODO this will break!
        prefix = f"{modfname}:{line}: UserWarning: "
        suffix = "\n  self.file, channels = load_from_file(fname)"
        msg = "Could not import jungfrau_utils, will treat JF files as regular files."
        msg = prefix + msg + suffix
        with self.assertPrintsError(msg):
            with SFDataFile(self.fname) as data:
                ch = data[self.det_name]
                self.assertTrue(
                    isinstance(ch, sfdata.sfchannel.SFChannel)
                )

        msg = "Could not import jungfrau_utils, will treat JF files as regular files."
        with self.assertWarns(msg):
            with SFDataFile(self.fname) as data:
                ch = data[self.det_name]
                self.assertTrue(
                    isinstance(ch, sfdata.sfchannel.SFChannel)
                )



