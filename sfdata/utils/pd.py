import numpy as np
import pandas as pd


BooleanDtype = pd.BooleanDtype()
StringDtype  = pd.StringDtype()


def decide_pandas_dtype(arr):
    if arr.ndim > 1: # ndim. columns need object dtype
        return object

    dtype = arr.dtype

    if np.issubdtype(dtype, np.floating):
        return dtype

    if np.issubdtype(dtype, np.integer):
        size = dtype.itemsize * 8 # itemsize is in bytes
        if np.issubdtype(dtype, np.unsignedinteger):
            return f"UInt{size}"
        return f"Int{size}"

    if np.issubdtype(dtype, bool): # covers: bool, np.bool and np.bool_
        return BooleanDtype

    if np.issubdtype(dtype, str): # covers: str, np.str and np.str_
        return StringDtype

    return object



