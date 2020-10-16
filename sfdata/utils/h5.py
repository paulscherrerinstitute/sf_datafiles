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



