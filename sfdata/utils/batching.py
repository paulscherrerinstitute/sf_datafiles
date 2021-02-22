import numpy as np
from .np import adjust_shape, nothing_like


def apply_batched(func, dataset, indices, batch_size, nbatches=None):
    """
    Iterate over dataset[indices] in batches of batch_size length
    and apply func to each batch collecting the results in a numpy array
    limit the result to nbatches batches, the default nbatches=None means all batches
    """
    if batch_size == 0 or nbatches == 0:
        return nothing_like(dataset)

    batches = batched(dataset, indices, batch_size, nbatches=nbatches)
    first_indices, first_batch = next(batches)
    first_batch_res = func(first_batch)

    ntotal = len(indices)
    if nbatches is not None:
        ntotal_batched = nbatches * batch_size
        ntotal = min(ntotal, ntotal_batched)

    single_res_shape = first_batch_res[0].shape
    res_shape = (ntotal, *single_res_shape)
    res = np.empty(res_shape)

    res[first_indices] = first_batch_res
    for indices, batch in batches:
        res[indices] = func(batch)
    return res


def batched(dataset, indices, batch_size, nbatches=None):
    """
    Iterate over dataset[indices] in batches of batch_size length
    limit the result to nbatches batches, the default nbatches=None means all batches
    """
    if batch_size == 0 or nbatches == 0:
        return

    ntotal = len(indices)
    batch_size = min(batch_size, ntotal)

    indices = np.asanyarray(indices) # see indices_in_batch below
    for i in range(0, ntotal, batch_size):
        if nbatches is not None and i >= nbatches * batch_size:
            break

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



