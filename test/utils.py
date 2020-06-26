import os
import ast
import tempfile
import unittest
import numpy as np
import pandas as pd


pd.options.mode.chained_assignment = "raise"
SettingWithCopyError = pd.core.common.SettingWithCopyError


identity = lambda iterable: iterable


def make_temp_filename(*args, **kwargs):
    fd, fname = tempfile.mkstemp(*args, **kwargs)
    os.close(fd)
    return fname


def read_names(fname):
    with open(fname, "r") as f:
        rb = f.read()
    rb = rb.split("\n")
    rb = [i for i in rb if i != ""]
    rb = set(rb)
    return rb


def eval_str(x):
    if isinstance(x, str):
        return ast.literal_eval(x)
    return x


def load_df_from_csv(fname):
    return pd.read_csv(fname, index_col=0, dtype=object).applymap(eval_str)



class TestCase(unittest.TestCase):

#    def assertAllTrue(self, test):
#        return self.assertTrue(all(test))

#    def assertNumpyAllTrue(self, test):
#        return self.assertTrue(np.all(test))

    def assertAllEqual(self, left, right):
        return np.testing.assert_array_equal(left, right)

    def assertNotRaises(self, *exc):
        if not exc:
            exc = (Exception,)
        return _AssertNotRaisesContext(self, *exc)



class _AssertNotRaisesContext:

    def __init__(self, testcase, exc):
        self.testcase = testcase
        self.exc = exc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            return # got no exception; counts as SUCCESS
        if not issubclass(exc_type, self.exc):
            return False # got the wrong type of exception, do not suppress it; counts as ERROR
        # got the right type of exception, test fails; counts as FAILURE
        self.testcase.fail("Unexpected exception: {}: {}".format(exc_type.__name__, exc_value))




