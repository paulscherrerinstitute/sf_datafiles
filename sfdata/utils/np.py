
def adjust_shape(arr):
    """transpose 1D column vectors to line vectors"""
    if arr.ndim == 2 and arr.shape[1] == 1:
        arr = arr.reshape(-1)
    return arr



