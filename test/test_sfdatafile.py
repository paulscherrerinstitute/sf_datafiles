#!/usr/bin/env python

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



