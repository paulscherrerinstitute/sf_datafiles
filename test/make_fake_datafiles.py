#!/usr/bin/env python

import h5py


def write_file(fname, data, pids, make_data=True):
    assert data.keys() == pids.keys()

    with h5py.File(fname, "w") as f:
        if make_data:
            gd = f.create_group("data")
        else:
            gd = f

        for cn in data.keys():
            gc = gd.create_group(cn)
            gcd = gc.create_dataset("data", data=data[cn])
            gcp = gc.create_dataset("pulse_id", data=pids[cn])



data = {
    "ch1": [0.1, 2.3, 4.5],
    "ch2": [[6.7], [8.9], [0.1]], # column vectors
    "ch3": [2.3, 4.5]
}

pids = {
    "ch1": [0, 1, 2],
    "ch2": [0, 1, 2],
    "ch3": [0, 2] # missing one pid here!
}

write_file("fake_data/run_test.SCALARS.h5", data, pids)



data = {
    "ch4": [[0.1, 2.3, 4.5], [6.7, 8.9, 0.1], [2.3, 4.5, 6.7]],
    "ch5": [
        [[0.1, 2.3, 4.5], [6.7, 8.9, 0.1], [2.3, 4.5, 6.7]], 
        [[8.9, 0.1, 2.3], [4.5, 6.7, 8.9], [0.1, 2.3, 4.5]], 
        [[6.7, 8.9, 0.1], [2.3, 4.5, 6.7], [8.9, 0.1, 2.3]]
    ],
    "ch6": [[0.1, 2.3, 4.5], [6.7, 8.9, 0.1]]
}

pids = {
    "ch4": [0, 1, 2],
    "ch5": [0, 1, 2],
    "ch6": [0, 2] # missing one pid here!
}

write_file("fake_data/run_test.ARRAYS.h5", data, pids, make_data=False)



