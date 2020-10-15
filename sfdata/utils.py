import numpy as np


def apply_to_batches(func, batches, ntotal): #TODO: this should probably be (func, dataset, indices, batch_size)
    first_indices, first_batch = next(batches)
    first_batch_res = func(first_batch)

    single_res_shape = first_batch_res[0].shape
    res_shape = (ntotal, *single_res_shape)
    res = np.empty(res_shape)

    res[first_indices] = first_batch_res
    for indices, batch in batches:
        res[indices] = func(batch)
    return res


def batcher(dataset, indices, batch_size):
    """
    Iterate over dataset[indices] in batches of batch_size length
    """
    indices = np.asanyarray(indices) # see indices_in_batch below
    for i in range(0, len(indices), batch_size):
        index_slice = slice(i, i+batch_size)
        batch_indices = indices[index_slice]

        # this assumes indices is sorted (otherwise min/max)
        start = batch_indices[0]
        stop  = batch_indices[-1] + 1

        slice_batch = slice(start, stop)
        indices_in_batch = batch_indices - start # indices has to be numpy array for this to work

        batch_data = dataset[slice_batch][indices_in_batch]
        batch_data = adjust_shape(batch_data)
        yield index_slice, batch_data


def adjust_shape(arr):
    """transpose 1D column vectors to line vectors"""
    if arr.ndim == 2 and arr.shape[1] == 1:
        arr = arr.reshape(-1)
    return arr


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



