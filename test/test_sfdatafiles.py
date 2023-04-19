#!/usr/bin/env python

from utils import TestCase, check_channel_closed
from consts import FNAME_ALL, FNAME_SCALARS, REPR_FILES, CH_1D_NAME, CH_1D_DATA, CH_ND_NAME, CH_ND_DATA1

import sfdata
from sfdata import SFDataFiles
from sfdata.errors import NoMatchingFileError


class TestSFDataFiles(TestCase):

    def run(self, *args, **kwargs):
        with SFDataFiles(FNAME_ALL) as data:
            self.data = data
            super().run(*args, **kwargs)

    def test_subset_across_files(self):
        subset = self.data[CH_1D_NAME, CH_ND_NAME]
        self.assertAllEqual(
            subset[CH_1D_NAME].data, CH_1D_DATA
        )
        self.assertAllEqual(
            subset[CH_ND_NAME].data[1], CH_ND_DATA1
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.data), REPR_FILES
        )


    def test_error(self):
        with self.assertRaises(NoMatchingFileError):
            SFDataFiles("does not exist")
        modfname = sfdata.sfdatafiles.__file__
        line = 77 #TODO this will break!
        prefix = f"{modfname}:{line}: UserWarning: "
        suffix = "\n  print_skip_warning(exc, quoted_fn)"
        broken_file = "fake_data/run_broken.SCALARS.h5"
        msg = f"Skipping \"{broken_file}\" since it caused OSError: Unable to open file (file signature not found)"
        msg = prefix + msg + suffix
        with self.assertRaises(NoMatchingFileError), self.assertPrintsError(msg):
            SFDataFiles(broken_file)

        msg = f"Skipping \"{broken_file}\" since it caused OSError: Unable to open file (file signature not found)"
        with self.assertRaises(NoMatchingFileError), self.assertWarns(msg):
            SFDataFiles(broken_file)


    def test_meta_optional(self):
        self.assertEqual(
            self.data.meta, None
        )

    def test_meta_exists(self): #TODO: better constants?
        with SFDataFiles("fake_data/run_meta.*.h5") as data:
            ref = {
                "g1": [10, 11, 12],
                "g2": [13, 14, 15, 16],
                "g3": [17, 18, 19],
                "g4": [30, 31, 32],
                "g5": [33, 34, 35, 36],
                "g6": [37, 38, 39],
            }
            for k in ref:
                self.assertAllEqual(
                    data.meta[k], ref[k]
                )


    def test_closed1(self):
        with SFDataFiles(FNAME_ALL) as data:
            ch = data[CH_1D_NAME]
        check_channel_closed(self, ch)

    def test_closed2(self):
        data = SFDataFiles(FNAME_ALL)
        ch = data[CH_1D_NAME]
        data.close()
        check_channel_closed(self, ch)

    def test_closed_twice(self):
        data = SFDataFiles(FNAME_ALL)
        ch = data[CH_1D_NAME]
        data.close()
        data.close()
        check_channel_closed(self, ch)

    def test_closed_wrong(self):
        data = SFDataFiles(FNAME_ALL)
        ch = data[CH_1D_NAME]
        for f in data.files:
            f.file.close() # close only h5 file
            f.close()      # also create ClosedH5, which cannot read file info
        check_channel_closed(self, ch)

    def test_closed_repr(self):
        with SFDataFiles(FNAME_SCALARS) as data:
            ch = data[CH_1D_NAME]
        rep = repr(ch._group)
        ref = 'Closed HDF5 group "/data/ch1" from file "fake_data/run_test.SCALARS.h5"'
        self.assertEqual(rep, ref)


    def test_warn_mask(self):
        msg = "The following channels from fake_data/run_test.SCALARS.h5 are masked by channels from fake_data/run_test.SCALARS.h5: ['ch1', 'ch2', 'ch3']"
        with self.assertWarns(msg):
            sfdata.sfdatafiles.load_files([FNAME_SCALARS, FNAME_SCALARS])



