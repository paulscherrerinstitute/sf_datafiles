#!/usr/bin/env python

import os
import io
import numpy as np
import unittest.mock

from utils import TestCase, identity, make_temp_filename, read_names, load_df_from_csv, SettingWithCopyError
from consts import FNAME_ALL, FNAME_SCALARS, FNAME_DF, CH_1D_COL_NAME, CH_1D_COL_DATA, CH_1D_NAME, CH_1D_PIDS, CH_1D_DATA, CH_ND_NAME, CH_ND_SHAPE, CH_ND_DATA1, REPR_CHANNEL

from sfdata import SFDataFiles
from sfdata.sfchannel import SFChannel, get_dataset, get_meta
from sfdata.errors import DatasetNotInGroupError


class TestSFChannel(TestCase):

    df_ref_lists = load_df_from_csv(FNAME_DF)

    df_ref_arrays = df_ref_lists.copy()
    for ch in df_ref_arrays:
        first_row_dat = df_ref_arrays[ch][0]
        if isinstance(first_row_dat, list):
            df_ref_arrays[ch] = [np.array(i) for i in df_ref_arrays[ch]]


    def run(self, *args, **kwargs):
        with SFDataFiles(FNAME_ALL) as data:
            self.data = data
            self.ch = data[CH_ND_NAME]
            super().run(*args, **kwargs)

    def test_read_one_channel_data(self):
        self.assertAllEqual(
            self.data[CH_1D_NAME].data, CH_1D_DATA
        )

    def test_read_one_channel_pids(self):
        self.assertAllEqual(
            self.data[CH_1D_NAME].pids, CH_1D_PIDS
        )

    def test_reset_valid(self):
        self.ch.valid = None
        self.ch.reset_valid()
        self.assertEqual(
            self.ch.valid, Ellipsis
        )

    def test_length(self):
        self.assertEqual(
            len(self.ch), self.ch.nvalid
        )
        self.assertEqual(
            len(self.ch), len(self.ch.pids)
        )

    def test_datasets_pids(self):
        self.assertEqual(
            self.ch.datasets.pids.shape, self.ch.pids.shape
        )
        self.assertEqual(
            self.ch.datasets.data.shape, self.ch.data.shape
        )

    def test_shape_all_valid(self):
        self.assertEqual(
            self.ch.shape, CH_ND_SHAPE
        )

    def test_shape_partial_valid(self):
        replacement_valid = [0, 1]
        new_shape = list(CH_ND_SHAPE)
        new_shape[0] = len(replacement_valid)
        new_shape = tuple(new_shape)
        self.ch.valid = replacement_valid
        self.assertEqual(
            self.ch.shape, new_shape
        )
        self.ch.reset_valid()

    def test_name(self):
        self.assertEqual(
            self.ch.name, CH_ND_NAME
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.ch), REPR_CHANNEL
        )


    def test_timestamps_optional(self):
        self.assertEqual(
            self.ch.timestamps, None
        )

    def test_timestamps_exists(self): #TODO: better constants?
        with SFDataFiles("fake_data/run_timestamps.SCALARS.h5") as data:
            ts = [
                "1970-01-01T00:00:00.000000100",
                "1970-01-01T00:00:00.000000101",
                "1970-01-01T00:00:00.000000102"
            ]
            ts = np.array(ts, dtype="datetime64[ns]")
            ch = data["ch1"]
            self.assertAllEqual(
                ch.timestamps, ts
            )


    def test_dataframe_setting(self):
        data = self.data
        methods = (data.to_dataframe, data.to_dataframe_accumulate, data.to_dataframe_fill)
        for func in methods:
            with self.assertNotRaises(SettingWithCopyError):
                func()


    @unittest.mock.patch("sfdata.sfdata.tqdm", identity)
    def test_to_dataframe(self):
        df_ref = self.df_ref_lists
        data = self.data
        methods = (data.to_dataframe, data.to_dataframe_accumulate, data.to_dataframe_fill)
        for func in methods:
            for as_lists in (True, False):
                for show_progress in (True, False):
                    df = func(as_lists=as_lists, show_progress=show_progress)
                    df.fillna(np.nan, inplace=True) #TODO: object array messes with df.equals below

                    self.assertEqual(
                        df.shape, df_ref.shape
                    )
                    self.assertAllEqual(
                        df.columns, df_ref.columns
                    )
                    self.assertAllEqual(
                        df.index, df_ref.index
                    )

                    if as_lists:
                        # here lst1 == lst2 works directly
                        self.assertTrue(
                            df.equals(df_ref)
                        )
                    else:
                        # check each entry array individually, otherwise: "The truth value of an array with more than one element is ambiguous."
                        for ch in df:
                            col = df[ch]
                            col_ref = df_ref[ch]
                            for row, row_ref in zip(col, col_ref):
                                self.assertAllEqual(row, row_ref)


    def test_to_dataframe_dtypes(self):
        with SFDataFiles("fake_data/run_dtypes.SCALARS.h5") as data:
            methods = (data.to_dataframe, data.to_dataframe_accumulate, data.to_dataframe_fill)
            for func in methods:
                df_objects  = func(as_nullable=False)
                df_nullable = func(as_nullable=True)

                for ch in df_objects:
                    dtype = df_objects[ch].dtype
                    self.assertEqual(
                        dtype, object
                    )

                for ch in df_nullable:
                    ref = ch[0] # first char in channel names is type code
                    dtype = df_nullable[ch].dtype
                    self.assertEqual(
                        dtype.kind, ref
                    )
                    str_dtype = str(dtype).lower()
                    char_dtype = str_dtype[0]
                    self.assertEqual(
                        char_dtype, ref
                    )


    @unittest.mock.patch("sfdata.sfdata.tqdm", identity)
    def test_to_xarray(self):
        #TODO: reference only works for 1D arrays
        xr_ref = self.df_ref_lists[["ch1", "ch2", "ch3"]].to_xarray().rename(index = "pids")
        data = self.data["ch1", "ch2", "ch3"]
        methods = (data.to_xarray, data.to_xarray_accumulate)
        for func in methods:
            for progress in (True, False):
                xr = func(show_progress=progress)

                self.assertEqual(
                    xr.sizes, xr_ref.sizes
                )
                self.assertEqual(
                    xr.dims, xr_ref.dims
                )
                self.assertAllEqual(
                    xr.coords, xr_ref.coords
                )
                self.assertAllEqual(
                    xr.indexes, xr_ref.indexes
                )
                self.assertTrue(
                    xr.equals(xr_ref)
                )


    def test_drop_missing(self):
        self.data.drop_missing()
        self.assertAllEqual(
            self.ch.valid, [0, 2]
        )
        self.data.reset_valid()
        self.assertEqual(
            self.ch.valid, Ellipsis
        )

    @unittest.mock.patch("sfdata.sfdata.tqdm", identity)
    def test_drop_missing_progressbar(self):
        self.data.drop_missing(show_progress=True)
        self.assertAllEqual(
            self.ch.valid, [0, 2]
        )
        self.data.reset_valid()
        self.assertEqual(
            self.ch.valid, Ellipsis
        )

    def test_save_names(self):
        with self.assertNotRaises():
            self.data.save_names("/dev/null", "w")

    def test_save_names_write_w(self):
        with self.assertNotRaises():
            fname = make_temp_filename(text=True)
            self.data.save_names(fname, "w")
            os.remove(fname)

    def test_save_names_write_x(self):
        with self.assertNotRaises():
            fname = make_temp_filename(text=True)
            os.remove(fname)
            self.data.save_names(fname, "x")
            os.remove(fname)

    def test_save_names_write_x_fail(self):
        fname = make_temp_filename(text=True)
        with self.assertRaises(FileExistsError):
            self.data.save_names(fname, "x")
        os.remove(fname)

    def test_save_names_write_r_exists_fail(self):
        fname = make_temp_filename(text=True)
        with self.assertRaises(io.UnsupportedOperation):
            self.data.save_names(fname, "r")
        os.remove(fname)

    def test_save_names_write_r_not_exists_fail(self):
        fname = make_temp_filename(text=True)
        os.remove(fname)
        with self.assertRaises(FileNotFoundError):
            self.data.save_names(fname, "r")

    def test_save_names_readback(self):
        fname = make_temp_filename(text=True)
        self.data.save_names(fname, "w")
        names = set(self.data.names)
        rb = read_names(fname)
        self.assertEqual(
            names, rb
        )
        os.remove(fname)


    def test_get_item_index(self):
        data = self.ch[1]
        self.assertAllEqual(
            data, CH_ND_DATA1
        )
        self.assertAllEqual(
            data, self.ch.data[1]
        )

    def test_get_item_tuple(self):
        data = self.ch[1, 1]
        self.assertAllEqual(
            data, CH_ND_DATA1[1]
        )
        self.assertAllEqual(
            data, self.ch.data[1, 1]
        )


    def test_read_column_vector(self):
        with SFDataFiles(FNAME_SCALARS) as data:
            self.assertAllEqual(
                data[CH_1D_COL_NAME].data, CH_1D_COL_DATA
            )


    def test_in_batches(self):
        for i in range(4):
            for j in range(4):
                n = i + 1
                m = j + 1

                res = []
                for index, batch in self.data[CH_1D_NAME].in_batches(n, m):
                    res.extend(batch)
                self.assertAllEqual(
                    res, CH_1D_DATA[:n*m]
                )


    def test_apply_in_batches(self):
        nop = lambda x: x
        for i in range(4):
            for j in range(4):
                n = i + 1
                m = j + 1

                res = self.data[CH_1D_NAME].apply_in_batches(nop, n, m)
                self.assertAllEqual(
                    res, CH_1D_DATA[:n*m]
                )


    def test_broken(self):
        ch = self.data[CH_1D_NAME]
        with self.assertNotRaises():
            SFChannel("test", ch._group)
        with self.assertRaises(DatasetNotInGroupError):
            SFChannel("test", ch.datasets.data)


    def test_iter(self):
        ch = self.data[CH_1D_NAME]
        gen = iter(ch)
        self.assertAllEqual(next(gen), ch.pids)
        self.assertAllEqual(next(gen), ch.data)
        with self.assertRaises(StopIteration):
            next(gen)


    def test_get_dataset(self):
        group = {"test": 123}
        self.assertEqual(
            get_dataset("test", group), 123
        )

    def test_get_dataset_missing(self):
        group = {}
        with self.assertRaises(DatasetNotInGroupError):
            get_dataset("test", group)


    def test_get_meta(self):
        res = {"test": 123}
        group = {"meta": res}
        self.assertEqual(
            get_meta(group), res
        )

    def test_get_meta_missing(self):
        group = {}
        self.assertEqual(
            get_meta(group), None
        )



