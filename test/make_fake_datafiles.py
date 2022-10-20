#!/usr/bin/env python

import os.path
import h5py


def write_file(fname, data, pids, timestamps=None, make_data=True):
    assert data.keys() == pids.keys()

    if os.path.exists(fname):
        print(f"{fname} exists... skipping!")
        return

    print(f"creating {fname} ...")
    with h5py.File(fname, "w") as f:
        if make_data:
            gd = f.create_group("data")
        else:
            gd = f

        for cn in data.keys():
            gc = gd.create_group(cn)
            gcd = gc.create_dataset("data", data=data[cn])
            gcp = gc.create_dataset("pulse_id", data=pids[cn])
            if timestamps:
                ts = timestamps.get(cn)
                if ts:
                    gct = gc.create_dataset("timestamp", data=ts)


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



timestamps = {
    "ch1": [100, 101, 102],
    "ch2": [100, 101, 102],
    "ch3": [100, 102]
}

write_file("fake_data/run_timestamps.SCALARS.h5", data, pids, timestamps=timestamps)



meta = {
    "m1": [0, 1, 2],
    "m2": [3, 4, 5, 6],
    "m3": [7, 8, 9],
}

fname = "fake_data/run_meta.SCALARS.h5"
if os.path.exists(fname):
    print(f"{fname} exists... skipping!")
else:
    write_file(fname, data, pids)
    with h5py.File(fname, "a") as f:
        g = f["data/ch1"]
        m = g.create_group("meta")
        for k, v in meta.items():
            m[k] = v



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



fname = "fake_data/run_spurious_chans.ARRAYS.h5"
if os.path.exists(fname):
    print(f"{fname} exists... skipping!")
else:
    write_file(fname, data, pids, make_data=False)
    spurious_channels = (
        "file_create_date", # timestamp (accidentally) is a group and not an attribute
        "pulse_id"          # spurious pulse_id group in bsread files
    )
    # add additional spurious "channels"
    try:
        with h5py.File(fname, "a") as f:
            for ch in spurious_channels:
                f.create_dataset(ch, data=[0])
    except OSError:
        pass


fname = "fake_data/run_spurious_chans_only.ARRAYS.h5"
# add spurious "channels"
if os.path.exists(fname):
    print(f"{fname} exists... skipping!")
else:
    with h5py.File(fname, "w") as f:
        for ch in spurious_channels:
            f.create_dataset(ch, data=[0])



data = {
    "ch1": [11, 12, 13, 14, 15],
    "ch2": [10, 11,     13, 14] # channel delayed by one shot
}

pids = {
    "ch1": [0, 1, 2, 3, 4],
    "ch2": [0, 1,    3, 4]
}

write_file("fake_data/run_offset.SCALARS.h5", data, pids)



#det_name = "JF13T01V01"
det_name = "JFxxx"
fname = f"fake_data/run_testjf.{det_name}.h5"

if os.path.exists(fname):
    print(f"{fname} exists... skipping!")
else:
    with h5py.File(fname, "w") as f:
        f.create_dataset("/general/detector_name", data=det_name.encode())
        gc = f.create_group(f"/data/{det_name}")
        gc.create_dataset("data", data=[10, 11, 12])
        gc.create_dataset("pulse_id", data=[0, 1, 2])
        gc.create_dataset("daq_rec", data=[[0, 1, 2], [0, 1, 2], [0, 1, 2]])



fname = f"fake_data/run_testjf_bad_frames.{det_name}.h5"

if os.path.exists(fname):
    print(f"{fname} exists... skipping!")
else:
    with h5py.File(fname, "w") as f:
        f.create_dataset("/general/detector_name", data=det_name.encode())
        gc = f.create_group(f"/data/{det_name}")
        gc.create_dataset("data", data=[10, 11, 12])
        gc.create_dataset("pulse_id", data=[0, 1, 2])
        gc.create_dataset("daq_rec", data=[[0, 1, 2], [0, 1, 2], [0, 1, 2]])
        gc.create_dataset("is_good_frame", data=[True, False, True])



# b: bool
# i: int
# f: float
data = {
    "b_ch1": [True] * 5,
    "b_ch2": [False] * 5,
    "b_ch3": [True, False, True, False, True],
    "b_ch4": [False, True, False, True, False],
    "b_ch3": [True, True, False, True],
    "b_ch4": [False, False, True, False],
    "i_ch1": [11, 12, 13, 14, 15],
    "i_ch2": [11, 12,     14, 15],
    "f_ch1": [11.1, 12.2, 13.3, 14.4, 15.5],
    "f_ch2": [11.1, 12.2, 13.3,       15.5],
}

pids = {
    "b_ch1": [0, 1, 2, 3, 4],
    "b_ch2": [0, 1, 2, 3, 4],
    "b_ch3": [0, 1, 2, 3, 4],
    "b_ch4": [0, 1, 2, 3, 4],
    "b_ch3": [0,    2, 3, 4],
    "b_ch4": [0,    2, 3, 4],
    "i_ch1": [0, 1, 2, 3, 4],
    "i_ch2": [0, 1,    3, 4],
    "f_ch1": [0, 1, 2, 3, 4],
    "f_ch2": [0, 1, 2,    4],
}

write_file("fake_data/run_dtypes.SCALARS.h5", data, pids)



