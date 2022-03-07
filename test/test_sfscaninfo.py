#!/usr/bin/env python

import unittest.mock

from utils import TestCase

import sfdata
from sfdata import SFScanInfo
from sfdata.errors import NoUsableFileError


class TestSFScanInfo(TestCase):

    nsteps = 3
    fname = "fake_data/run_test.json"
    scan = SFScanInfo(fname)

    def test_loop(self):
        with self.assertNotRaises():
            for step in self.scan:
                pass

    def test_getitem(self):
        with self.assertNotRaises():
            step = self.scan[0]

        for i, ref in enumerate(self.scan):
            step = self.scan[i]
            for sf, rf in zip(step.files, ref.files):
                self.assertEqual(sf.file, rf.file)

    def test_slice(self):
        with self.assertNotRaises():
            scan_slice = self.scan[1: ]
            scan_slice = self.scan[ :1]
            scan_slice = self.scan[1:2]

        scan_iter = iter(self.scan)
        next(scan_iter) # skip first entry of iterator

        scan_slice = self.scan[1: ] # slice starts from second entry
        for step, ref in zip(scan_slice, scan_iter):
            for sf, rf in zip(step.files, ref.files):
                self.assertEqual(sf.file, rf.file)

    def test_length(self):
        self.assertEqual(
            len(self.scan), self.nsteps
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.scan), f"SFScanInfo(\"{self.fname}\"): {self.nsteps} steps"
        )


    @unittest.mock.patch("sfdata.SFDataFiles.__init__", side_effect=Exception("test"))
    def test_broken(self, _):
#        self.maxDiff = None
        modfname = sfdata.sfscaninfo.__file__
        line = 57 #TODO this will break!
        prefix = f"{modfname}:{line}: UserWarning: "
        suffix = "\n  print_skip_warning(exc, sn)"
        msg_fmt = "Skipping step {} ['fake_data/run_test.ARRAYS.h5', 'fake_data/run_test.SCALARS.h5'] since it caused Exception: test"
        msg_fmt = prefix + msg_fmt + suffix
        msg = (msg_fmt.format(i) for i in range(self.nsteps))
        with self.assertRaises(NoUsableFileError), self.assertPrintsError(*msg):
            for step in self.scan:
                pass

        msg_fmt = "Skipping step {} ['fake_data/run_test.ARRAYS.h5', 'fake_data/run_test.SCALARS.h5'] since it caused Exception: test"
        msg = (msg_fmt.format(i) for i in range(self.nsteps))
        with self.assertRaises(NoUsableFileError), self.assertWarns(*msg):
            for step in self.scan:
                pass


    def test_no_files(self):
#        self.maxDiff = None
        modfname = sfdata.sfscaninfo.__file__
        line = 57 #TODO this will break!
        prefix = f"{modfname}:{line}: UserWarning: "
        suffix = "\n  print_skip_warning(exc, sn)"
        msg_fmt = "Skipping step {} ['does not exist'] since it caused NoMatchingFileError: No matching file for patterns: \"does not exist\""
        msg_fmt = prefix + msg_fmt + suffix
        msg = (msg_fmt.format(i) for i in range(self.nsteps))
        empty = SFScanInfo("fake_data/run_no_files.json")
        with self.assertRaises(NoUsableFileError), self.assertPrintsError(*msg):
            for step in empty:
                pass

        msg_fmt = "Skipping step {} ['does not exist'] since it caused NoMatchingFileError: No matching file for patterns: \"does not exist\""
        msg = (msg_fmt.format(i) for i in range(self.nsteps))
        with self.assertRaises(NoUsableFileError), self.assertWarns(*msg):
            for step in empty:
                pass



