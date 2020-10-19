import numpy as np


def adjust_shape(arr):
    """transpose 1D column vectors to line vectors"""
    arr = np.asanyarray(arr)
    if arr.ndim == 2 and arr.shape[1] == 1:
        arr = arr.reshape(-1)
    return arr



