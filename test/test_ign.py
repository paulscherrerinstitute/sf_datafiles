#!/usr/bin/env python

import unittest.mock

from utils import TestCase

import sfdata
from sfdata.ign import remove_ignored_filetypes_scan, remove_ignored_filetypes_run, split_filetypes_scan, split_filetypes_run
from sfdata.ign import warn_ignore, get_filetype, make_printable_nfiles


class TestIgn(TestCase):

    def test_remove_ignored_filetypes_scan(self):
        allowed = ["a", "b", "c"]
        forbidden = ["test.PVCHANNELS.h5"]
        self.assertEqual(
            remove_ignored_filetypes_scan([allowed] * 3), [allowed] * 3
        )
        msg = "will ignore 3 files over the whole scan of the type: PVCHANNELS"
        with self.assertWarns(msg):
            self.assertEqual(
                remove_ignored_filetypes_scan([allowed + forbidden] * 3), [allowed] * 3
            )

    def test_remove_ignored_filetypes_run(self):
        allowed = ["a", "b", "c"]
        forbidden = ["test.PVCHANNELS.h5"]
        self.assertEqual(
            remove_ignored_filetypes_run(allowed), allowed
        )
        msg = "will ignore 1 file for this run of the type: PVCHANNELS"
        with self.assertWarns(msg):
            self.assertEqual(
                remove_ignored_filetypes_run(allowed + forbidden), allowed
            )
        msg = "will ignore 3 files for this run of the type: PVCHANNELS"
        with self.assertWarns(msg):
            self.assertEqual(
                remove_ignored_filetypes_run(allowed + forbidden*3), allowed
            )
        msg = "will ignore 1 file for this run of the type: PVCHANNELS"
        with self.assertWarns(msg):
            self.assertEqual(
                remove_ignored_filetypes_run(forbidden), []
            )


    def test_split_filetypes_scan(self):
        allowed = ["a", "b", "c"]
        forbidden = ["test.PVCHANNELS.h5"]
        self.assertEqual(
            split_filetypes_scan([allowed] * 3), ([allowed] * 3, 0)
        )
        self.assertEqual(
            split_filetypes_scan([allowed + forbidden] * 3), ([allowed] * 3, 3)
        )

    def test_split_filetypes_run(self):
        allowed = ["a", "b", "c"]
        forbidden = ["test.PVCHANNELS.h5"]
        self.assertEqual(
            split_filetypes_run(allowed), (allowed, 0)
        )
        self.assertEqual(
            split_filetypes_run(allowed + forbidden), (allowed, 1)
        )
        self.assertEqual(
            split_filetypes_run(allowed + forbidden*3), (allowed, 3)
        )
        self.assertEqual(
            split_filetypes_run(forbidden), ([], 1)
        )


    # test this separately because the warn_ignore tests depend on it
    def test_consts(self):
        self.assertEqual(
            sfdata.ign.IGNORED_FILETYPES, ["PVCHANNELS"]
        )
        self.assertEqual(
            sfdata.ign.PRINTABLE_IGNORED_FILETYPES, "PVCHANNELS"
        )

    def test_warn_ignore(self):
        msg = "will ignore 0 files A_TEST of the type: PVCHANNELS"
        with self.assertWarns(msg):
            warn_ignore(0, "A_TEST")

    @unittest.mock.patch("sfdata.ign.IGNORED_FILETYPES", ["X", "Y", "Z"])
    @unittest.mock.patch("sfdata.ign.PRINTABLE_IGNORED_FILETYPES", "TEST")
    def test_warn_ignore_consts(self):
        msg = "will ignore 10 files A_TEST of the types: TEST"
        with self.assertWarns(msg):
            warn_ignore(10, "A_TEST")


    def test_get_filetype(self):
        self.assertEqual(
            get_filetype("a.b.c"), "b"
        )
        self.assertEqual(
            get_filetype("a.b"), "a"
        )
        self.assertEqual(
            get_filetype("a"), None
        )


    def test_make_printable_nfiles(self):
        self.assertEqual(
            make_printable_nfiles(0), "0 files"
        )
        self.assertEqual(
            make_printable_nfiles(1), "1 file"
        )
        self.assertEqual(
            make_printable_nfiles(2), "2 files"
        )



