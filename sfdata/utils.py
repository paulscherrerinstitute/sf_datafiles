import numpy as np


def h5_boolean_indexing(ds, indices):
    """
    hdf5 does not support boolean indexing on the first axis for n-dim. datasets:
    https://github.com/h5py/h5py/issues/626
    This function calculates the positions of the Trues in the boolean indices 
    and uses those as coordinates within the dataset.
    If ds is 1D, the indices will be applied as is.
    """
    if ds.ndim == 1:
        return ds[indices]
    indices = np.asanyarray(indices)
    assert indices.ndim == 1, "indices needs to be 1D"
    coords = np.nonzero(indices)[0].tolist()
    return ds[coords]


def typename(obj):
    return type(obj).__name__


def bar(perc, block="▇", n_blocks_total=10):
    n = _n_blocks(perc, n_blocks_total)
    return block * n

def dip(perc, block="▇", n_blocks_total=10):
    n = _n_blocks(perc, n_blocks_total)
    n = n_blocks_total - n
    return block * n

def _n_blocks(perc, n_blocks_total):
    divider = 100 / n_blocks_total
    return int(np.ceil(perc / divider))


def percentage(n, ntotal, decimals=0):
    ratio = n / ntotal
    return _percentage(ratio, decimals)

def percentage_missing(n, ntotal, decimals=0):
    ratio = n / ntotal
    ratio = 1 - ratio
    return _percentage(ratio, decimals)

def _percentage(ratio, decimals):
    ratio *= 100
    ratio = round(ratio, decimals)
    if decimals == 0:
        return int(ratio)
    return ratio


def decide_color(n, nmin, nmax): #TODO: more level? decide upon percentages?
    if n == nmax:
        return "green"
    elif n == nmin:
        return "red"
    else:
        return None


def strlen(val):
    return len(str(val))

def maxstrlen(iterable):
    return max(strlen(i) for i in iterable)


def print_line(length=80, char="-"):
    print("\n" + char*length + "\n")


def printable_string_sequence(strings):
    strings = (nice_string_repr(s) for s in strings)
    return ", ".join(strings)

def nice_string_repr(string):
    return repr(string).replace("'", '"')



