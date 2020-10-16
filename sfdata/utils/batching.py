import numpy as np
from .np import adjust_shape


def apply_batched(func, dataset, indices, batch_size):
    """
    Iterate over dataset[indices] in batches of batch_size length
    and apply func to each batch collecting the results in a numpy array
    """
    batches = batched(dataset, indices, batch_size)
    first_indices, first_batch = next(batches)
    first_batch_res = func(first_batch)

    ntotal = len(indices)
    single_res_shape = first_batch_res[0].shape
    res_shape = (ntotal, *single_res_shape)
    res = np.empty(res_shape)

    res[first_indices] = first_batch_res
    for indices, batch in batches:
        res[indices] = func(batch)
    return res


def batched(dataset, indices, batch_size):
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



