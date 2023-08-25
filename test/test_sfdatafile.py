#!/usr/bin/env python

import unittest
import sys

from utils import TestCase, check_channel_closed
from hiddenmod import HiddenModule
from consts import FNAME_SCALARS, REPR_FILE, CH_1D_NAME, CH_1D_DATA, CH_1D_COL_NAME

from sfdata import SFDataFile
from sfdata.errors import NoUsableChannelError


class TestSFDataFile(TestCase):

    def run(self, *args, **kwargs):
        with SFDataFile(FNAME_SCALARS) as data:
            self.data = data
            super().run(*args, **kwargs)

    def test_subset(self):
        subset = self.data[CH_1D_NAME, CH_1D_COL_NAME]
        self.assertAllEqual(
            subset[CH_1D_NAME].data, CH_1D_DATA
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.data), REPR_FILE
        )


    def test_meta_optional(self):
        self.assertEqual(
            self.data.meta, None
        )

    def test_meta_exists(self): #TODO: better constants?
        with SFDataFile("fake_data/run_meta.SCALARS.h5") as data:
            ref = {
                "g1": [10, 11, 12],
                "g2": [13, 14, 15, 16],
                "g3": [17, 18, 19],
            }
            for k in ref:
                self.assertAllEqual(
                    data.meta[k], ref[k]
                )


    def test_closed1(self):
        with SFDataFile(FNAME_SCALARS) as data:
            ch = data[CH_1D_NAME]
        check_channel_closed(self, ch)

    def test_closed2(self):
        data = SFDataFile(FNAME_SCALARS)
        ch = data[CH_1D_NAME]
        data.close()
        check_channel_closed(self, ch)

    def test_closed_twice(self):
        data = SFDataFile(FNAME_SCALARS)
        ch = data[CH_1D_NAME]
        data.close()
        data.close()
        check_channel_closed(self, ch)

    def test_closed_wrong(self):
        data = SFDataFile(FNAME_SCALARS)
        ch = data[CH_1D_NAME]
        data.file.close() # close only h5 file
        data.close()      # also create ClosedH5, which cannot read file info
        check_channel_closed(self, ch)

    def test_closed_repr(self):
        with SFDataFile(FNAME_SCALARS) as data:
            ch = data[CH_1D_NAME]
        rep = repr(ch._group)
        ref = 'Closed HDF5 group "/data/ch1" from file "fake_data/run_test.SCALARS.h5"'
        self.assertEqual(rep, ref)


    def test_spurious_chans(self):
        msg = [
            'Skipping channel "file_create_date" since it caused DatasetNotInGroupError: Cannot get dataset "data" from: <HDF5 dataset "file_create_date": shape (1,), type "<i8">',
            'Skipping channel "pulse_id" since it caused DatasetNotInGroupError: Cannot get dataset "data" from: <HDF5 dataset "pulse_id": shape (1,), type "<i8">'
        ]
        with self.assertWarns(*msg):
            with SFDataFile("fake_data/run_spurious_chans.ARRAYS.h5") as data:
                self.assertTrue("file_create_date" not in data)
                self.assertTrue("pulse_id" not in data)
        with self.assertRaises(NoUsableChannelError), self.assertWarns(*msg):
            with SFDataFile("fake_data/run_spurious_chans_only.ARRAYS.h5") as data:
                pass

    def test_missing_ju_import(self):
        import sfdata.sfdatafile
        self.assertNotEqual(
            sfdata.sfdatafile.ju, None
        )

        with HiddenModule("jungfrau_utils"):
            del sys.modules["sfdata.sfdatafile"]
            import sfdata.sfdatafile
            self.assertEqual(
                sfdata.sfdatafile.ju, None
            )

        del sys.modules["sfdata.sfdatafile"]
        import sfdata.sfdatafile
        self.assertNotEqual(
            sfdata.sfdatafile.ju, None
        )


    @unittest.mock.patch("jungfrau_utils.File.detector_name", "JF_ROI0")
    @unittest.mock.patch("jungfrau_utils.file_adapter.JFDataHandler")
    @unittest.mock.patch("jungfrau_utils.file_adapter.locate_gain_file", lambda path: "fn_gain")
    @unittest.mock.patch("jungfrau_utils.file_adapter.locate_pedestal_file", lambda path: "fn_pedestal")
    def test_multiple_JF_chans(self, _):
        with SFDataFile("fake_data/run_testjf.JF_ROI.h5") as data:
            self.assertEqual(
                sorted(data.names), ["JF_ROI0", "JF_ROI1", "JF_ROI2"]
            )

            # h5 group
            meta = data.file["general"]

            ref = {
                "g4": [30, 31, 32],
                "g5": [33, 34, 35, 36],
                "g6": [37, 38, 39],
            }

            for k in ref:
                self.assertAllEqual(
                    meta[k], ref[k]
                )

            # file meta
            meta = data.meta

            ref = {
                "g4": [30, 31, 32],
                "g5": [33, 34, 35, 36],
                "g6": [37, 38, 39],
            }

            for k in ref:
                self.assertAllEqual(
                    meta[k], ref[k]
                )

            # channel meta
            ch = data["JF_ROI0"]
            meta = ch.meta

            ref = {
                "m4": [20, 21, 22],
                "m5": [23, 24, 25, 26],
                "m6": [27, 28, 29],
            }

            for k in ref:
                self.assertAllEqual(
                    meta[k], ref[k]
                )



