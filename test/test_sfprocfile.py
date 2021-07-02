#!/usr/bin/env python

import os
import h5py

from utils import TestCase

from sfdata import SFProcFile
from sfdata.errors import ArrayLengthMismatch


FNAME = "tmp_test_sfprocfile.h5"
CHNAME = "test"
PIDS = [0, 1, 2]
DATA = [3, 4, 5]


def read_h5_data(fname, name):
    with h5py.File(fname, "r") as f:
        pids = f[f"/data/{name}/pulse_id"][:]
        data = f[f"/data/{name}/data"][:]
    return pids, data

def read_h5_meta(fname, name):
    with h5py.File(fname, "r") as f:
        value = f[f"/meta/{name}"][:]
    return value

def read_h5_attr(fname, name):
    with h5py.File(fname, "r") as f:
        value = f.attrs[name]
    return value



class TestSFProcFile(TestCase):

    def _assertPidsData(self, name):
        read_pids, read_data = read_h5_data(FNAME, name)
        self.assertAllEqual(read_pids, PIDS)
        self.assertAllEqual(read_data, DATA)

    def _assertMeta(self, name):
        read_data = read_h5_meta(FNAME, name)
        self.assertAllEqual(read_data, DATA)

    def _assertAttr(self, name):
        read_data = read_h5_attr(FNAME, name)
        self.assertAllEqual(read_data, DATA)


    def test_creation_manual(self):
        with self.assertCreatesTempFile(FNAME):
            f = SFProcFile(FNAME)
            f.close()

    def test_creation_context(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                pass

    def test_creation_invalid_mode(self):
        with self.assertRaises(ValueError):
            SFProcFile(FNAME, mode="invalid")


    def test_add_channel(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_channel(CHNAME, PIDS, DATA)
            self._assertPidsData(CHNAME)

    def test_add_channel_length_mismatch(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(ArrayLengthMismatch):
                    f.add_channel(CHNAME, PIDS, [])
                with self.assertRaises(ArrayLengthMismatch):
                    f.add_channel(CHNAME, [], DATA)


    def test_add_channels_one_dict(self):
        names = [CHNAME + str(i) for i in range(5)]
        chans = {n: (PIDS, DATA) for n in names}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_channels(chans)

            for n in names:
                self._assertPidsData(n)


    def test_add_channels_two_dicts(self):
        names = [CHNAME + str(i) for i in range(5)]
        dpids = {n: PIDS for n in names}
        ddata = {n: DATA for n in names}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_channels(dpids, ddata)

            for n in names:
                self._assertPidsData(n)


    def test_add_channels_two_dicts_keyerror_short_pids(self):
        names = [CHNAME + str(i) for i in range(5)]
        dpids = {n: PIDS for n in names[1:]}
        ddata = {n: DATA for n in names}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(KeyError):
                    f.add_channels(dpids, ddata)


    def test_add_channels_two_dicts_keyerror_short_data(self):
        names = [CHNAME + str(i) for i in range(5)]
        dpids = {n: PIDS for n in names}
        ddata = {n: DATA for n in names[1:]}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(KeyError):
                    f.add_channels(dpids, ddata)


    def test_add_channels_two_dicts_keyerror_differing_keys(self):
        names = [CHNAME + str(i) for i in range(5)]
        dpids = {n: PIDS for n in names[1:]}
        ddata = {n: DATA for n in names[:-1]}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(KeyError):
                    f.add_channels(dpids, ddata)


    def test_add_channels_n_kwargs(self):
        names = [CHNAME + str(i) for i in range(5)]
        chans = {n: (PIDS, DATA) for n in names}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_channels(**chans)

            for n in names:
                self._assertPidsData(n)


    def test_add_channels_args_error(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(TypeError):
                    f.add_channels(1, 2, 3)


    def test_add_meta_entry(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_meta_entry(CHNAME, DATA)

            self._assertMeta(CHNAME)


    def test_add_meta_entries_one_dict(self):
        names = [CHNAME + str(i) for i in range(5)]
        entries = {n: DATA for n in names}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_meta_entries(entries)

            for n in names:
                self._assertMeta(n)


    def test_add_meta_entries_n_kwargs(self):
        names = [CHNAME + str(i) for i in range(5)]
        entries = {n: DATA for n in names}

        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_meta_entries(**entries)

            for n in names:
                self._assertMeta(n)


    def test_add_meta_entries_args_error(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(TypeError):
                    f.add_meta_entries(1, 2)


    def test_add_attrs(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.attrs[CHNAME] = DATA

            self._assertAttr(CHNAME)


    def test_length(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                self.assertEqual(len(f), 0)
                f.add_channel(CHNAME, PIDS, DATA)
                self.assertEqual(len(f), 1)

    def test_repr(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                self.assertEqual(repr(f), f"SFProcFile(\"{FNAME}\"): 0 channels")
                f.add_channel(CHNAME, PIDS, DATA)
                self.assertEqual(repr(f), f"SFProcFile(\"{FNAME}\"): 1 channels")

    def test_getitem(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f.add_channel(CHNAME, PIDS, DATA)
                ch = f[CHNAME]
                self.assertEqual(repr(ch), f"SFChannel: {CHNAME}")

    def test_getitem_empty(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(KeyError):
                    f[CHNAME]

    def test_setitem(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                f[CHNAME] = (PIDS, DATA)
            self._assertPidsData(CHNAME)

    def test_drop_missing_error(self):
        with self.assertCreatesTempFile(FNAME):
            with SFProcFile(FNAME) as f:
                with self.assertRaises(NotImplementedError):
                    f.drop_missing()



