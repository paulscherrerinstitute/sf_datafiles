#!/usr/bin/env python

import numpy as np
import pandas as pd

from utils import TestCase
from consts import FNAME_ARRAYS, FNAME_SCALARS, CH_ND_DATA1

from sfdata import SFDataFile
from sfdata.utils import print_line, cprint, typename, maxstrlen, strlen, percentage_missing, dip, decide_color, json_load, h5_boolean_indexing, decide_pandas_dtype, apply_batched, batched
from sfdata.utils.np import nothing_like
from sfdata.utils.progress import bar, percentage # not actually used anywhere


class TestUtils(TestCase):

    def test_typename(self):
        class SomeClass: pass
        some_object = SomeClass()
        self.assertEqual(
            typename(some_object), "SomeClass"
        )

    def test_h5_boolean_indexing_1d(self):
        """
        For 1D boolean indexing into hdf5 is possible, 
        so compare function result with straight forward applying the index
        """
        with SFDataFile(FNAME_SCALARS) as data:
            ch = data["ch1"]
            pids = ch.pids
            bool_indices = (pids == 1)
            ds = ch.datasets.data
            self.assertEqual(
                h5_boolean_indexing(ds, bool_indices), ds[bool_indices]
            )
            bool_indices = np.ones(len(ds)).astype(bool)
            self.assertAllEqual(
                h5_boolean_indexing(ds, bool_indices), ds[:]
            )

    def test_h5_boolean_indexing_nd(self):
        """
        For nD boolean indexing into hdf5 is not possible,
        so compare function result to hard-coded values
        """
        with SFDataFile(FNAME_ARRAYS) as data:
            ch = data["ch5"]
            pids = ch.pids
            bool_indices = (pids == 1)
            ds = ch.datasets.data
            self.assertAllEqual(
                h5_boolean_indexing(ds, bool_indices), [CH_ND_DATA1]
            )
            bool_indices = np.ones(len(ds)).astype(bool)
            self.assertAllEqual(
                h5_boolean_indexing(ds, bool_indices), ds[:]
            )


    def test_np_nothing_like(self):
        for dtype in (float, int):
            ref = np.empty(0, dtype=dtype)
            arr = np.ones((2, 2), dtype=dtype)
            nl = nothing_like(arr)
            self.assertAllEqual(
                nl, ref
            )


    def test_json_load(self):
        ref = {
            "test int": 1,
            "test float": 1.23,
            "test dict": {
                "element": "test"
            },
            "test none": None
        }
        data = json_load("fake_data/test.json")
        self.assertEqual(data, ref)


    def test_strlen(self):
        self.assertEqual(strlen("test"), 4)

    def test_maxstrlen(self):
        strings = ("test", "tes", "te", "t")
        self.assertEqual(maxstrlen(strings), 4)

    def test_print_line(self):
        with self.assertStdout("\n" + 80 * "-" + "\n\n"):
            print_line()
        with self.assertStdout("\nxxx\n\n"):
            print_line(3, "x")


    def test_cprint(self):
        with self.assertStdout("\x1b[32mtest\x1b[39m\n"):
            cprint("test", color="green")
        with self.assertStdout("\x1b[31mtest\x1b[39m\n"):
            cprint("test", color="red")
        with self.assertRaises(ValueError):
            cprint("test", color="not a color")


    def test_progress_dip(self):
        block = "▇"
        res = dip(0)
        self.assertEqual(res, block * 10)
        res = dip(10)
        self.assertEqual(res, block * 9)
        res = dip(100)
        self.assertEqual(res, "")
        res = dip(50, block="x", n_blocks_total=2)
        self.assertEqual(res, "x")

    def test_progress_bar(self):
        block = "▇"
        res = bar(0)
        self.assertEqual(res, "")
        res = bar(10)
        self.assertEqual(res, block)
        res = bar(100)
        self.assertEqual(res, block * 10)
        res = bar(50, block="x", n_blocks_total=2)
        self.assertEqual(res, "x")

    def test_progress_decide_color(self):
        nmin, nmax = -1, 1
        c = decide_color(-1, nmin, nmax)
        self.assertEqual(c, "red")
        c = decide_color( 0, nmin, nmax)
        self.assertEqual(c, None)
        c = decide_color(+1, nmin, nmax)
        self.assertEqual(c, "green")

    def test_progress_percentage_missing(self):
        ntotal = 1000
        pm = percentage_missing(ntotal, ntotal)
        self.assertEqual(pm, 0)
        pm = percentage_missing(0, ntotal)
        self.assertEqual(pm, 100)
        pm = percentage_missing(333, ntotal, decimals=0)
        self.assertEqual(pm, 67)
        pm = percentage_missing(333, ntotal, decimals=1)
        self.assertEqual(pm, 66.7)
        pm = percentage_missing(333, ntotal, decimals=2)
        self.assertEqual(pm, 66.7)

    def test_progress_percentage(self):
        ntotal = 1000
        pm = percentage(ntotal, ntotal)
        self.assertEqual(pm, 100)
        pm = percentage(0, ntotal)
        self.assertEqual(pm, 0)
        pm = percentage(333, ntotal, decimals=0)
        self.assertEqual(pm, 33)
        pm = percentage(333, ntotal, decimals=1)
        self.assertEqual(pm, 33.3)
        pm = percentage(333, ntotal, decimals=2)
        self.assertEqual(pm, 33.3)


    def test_apply_batched(self):
        arr = np.arange(3)
        nop = lambda x: x

        res = apply_batched(nop, arr, arr, 0)
        self.assertAllEqual(res, [])

        res = apply_batched(nop, arr, arr, 1, nbatches=0)
        self.assertAllEqual(res, [])

        for i in range(4):
            for j in range(4):
                n = i + 1
                m = j + 1

                res = apply_batched(nop, arr, arr, m) # result is independent of batch size
                self.assertAllEqual(res, arr)

                res = apply_batched(nop, arr, arr, 1, nbatches=n)
                self.assertAllEqual(res, arr[:n])

                res = apply_batched(nop, arr, arr, 1, nbatches=100) # asking for too many batches
                self.assertAllEqual(res, arr)

                res = apply_batched(nop, arr, arr, m, nbatches=n)
                self.assertAllEqual(res, arr[:m*n])


    def test_batched(self):
        arr = np.arange(3)

        res = list(batched(arr, arr, 0)) # batch size zero -> nothing
        self.assertEqual(res, [])

        res = list(batched(arr, arr, 1, nbatches=0)) # number of batches zero -> nothing
        self.assertEqual(res, [])

        def compare(left, right):
            self.assertEqual(len(left), len(right))
            for l, r in zip(left, right):
                lind, larr = l
                rind, rarr = r
                self.assertEqual(lind, rind)
                self.assertAllEqual(larr, rarr)

        refs = [
            [ # n = 1
                (slice(0, 1), [0]),
                (slice(1, 2), [1]),
                (slice(2, 3), [2])
            ], [ # n = 2
                (slice(0, 2), [0, 1]),
                (slice(2, 4), [2])
            ], [ # n = 3
                (slice(0, 3), [0, 1, 2])
            ], [ # n = 4 (same as 3)
                (slice(0, 3), [0, 1, 2])
            ]
        ]

        for i, ref in enumerate(refs):
            n = i + 1
            res = list(batched(arr, arr, n))
            compare(res, ref)
            res = list(batched(arr, arr, n, nbatches=100)) # asking for too many batches
            compare(res, ref)
            res = list(batched(arr, arr, n, nbatches=1)) # asking only for first batch
            compare(res, ref[:1])


    def test_decide_pandas_dtype(self):
        base_arr = np.arange(4)

        arr = base_arr.reshape(2, 2)
        res = decide_pandas_dtype(arr)
        self.assertEqual(res, object)

        class NotCoveredType:
            pass

        mapping = {
            object: object,
            bool: pd.BooleanDtype(),
            str: pd.StringDtype(),
            float: float,
            int: "Int64",
            np.int8: "Int8",
            np.uint16: "UInt16",
            NotCoveredType: object
        }

        for tin, tout in mapping.items():
            arr = base_arr.astype(tin)
            res = decide_pandas_dtype(arr)
            self.assertEqual(res, tout)



