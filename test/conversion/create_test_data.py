#!/usr/bin/env python3

from random import choice
import numpy as np
import h5py


def split(A, i):
    return A[:i], A[i:]

def remove(i, A):
    left, right = split(A, i)
    return np.concatenate((left, right[1:]))


nchan = 10
ndata = 200
img_size = 50
ndrop = ndata // 10

with h5py.File("test_dump.h5", "w") as f:
    for c in range(nchan):
        name = f"ch{c}"
        print(name)

        pids = np.arange(ndata, dtype=int)
        data = np.random.rand(ndata, img_size, img_size)
#        print(pids.shape, data.shape)

        for _ in range(ndrop):
            n = len(pids)
            i = int(choice(range(n)))

            pids = remove(i, pids)
            data = remove(i, data)
            print(i, pids.shape, data.shape)

        base = "data/" + name
        f[base + "/data"] = data
        f[base + "/pulse_id"] = pids



