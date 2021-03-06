#!/usr/bin/env python3

# mprof run --interval 0.01 ./prof_conv.py
# mprof plot


import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("filename", nargs='?', default="test_dump.h5", help="name of the file to run the profiling on")

clargs = parser.parse_args()


try:
    profile # running via mprof / import breaks plotting (missing timestamps)
except NameError:
    from memory_profiler import profile


import os
import sys

this_dir = os.path.dirname(__file__)
sys.path.insert(0, (os.path.join(this_dir, "../..")))

from sfdata import SFDataFile



def convprof(fname):
    sfd = SFDataFile(fname)

    run_all(
        sfd.to_dataframe,
        sfd.to_dataframe_accumulate,
        sfd.to_dataframe_fill
    )

    run_all(
        sfd.to_xarray,
        sfd.to_xarray_accumulate
    )


def run_all(*funcs):
    ref_func = funcs[0]
    ref = create(ref_func)
    for f in funcs:
        run(f, ref)
    del ref


def run(func, ref):
    val = create(func)
    del val # create it twice as consistency check
    val = create(func)
    check(val, ref)


def create(ofunc):
    def func(*args, **kwargs): # SFDataFile is not hashable?
        return ofunc(*args, **kwargs)
    func.__name__ = ofunc.__name__
    func = profile(func)

    def fillna(val, fill_value=-1):
        return val.fillna(fill_value)
    fillna.__name__ = fillna.__name__ + "__" + ofunc.__name__ # assign fillnas to func
    fillna = profile(fillna)

    val = func(show_progress=True)
    val = fillna(val)
    return val


def check(val, ref):
    try:
        assert val.equals(ref)
    except AssertionError:
        print(f"\n{ref}\n{val}\n")





if __name__ == "__main__":
    fname = clargs.filename
    if not os.path.isfile(fname):
        msg = f"File \"{fname}\" does not exist. The script \"create_test_data.py\" may be used to create a default test file \"test_dump.h5\"."
        raise ValueError(msg)
    convprof(fname)



