#!/usr/bin/env python3

from sfdata import SFProcFile


pids = [0, 1, 2]
data = [3, 4, 5]


with SFProcFile("test.h5") as f:

    ## dict-like interfaces

    # add single channel
    f["ch1"] = (pids, data)

    # add single meta data entry
    f.meta["m1"] = data

    # add multiple meta data entries via kwargs
    f.meta.update(m2=data, m3=data)

    # add multiple meta data entries from dict
    entries = {
        "m4": data,
        "m5": data
    }
    f.meta.update(**entries)

    # add single attribute
    f.attrs["a1"] = 1

    # add multiple attributes via kwargs
    f.attrs.update(a2=2, a3=3)

    # add multiple attributes from dict
    attrs = {
        "a4": 4,
        "a5": 5
    }
    f.attrs.update(**attrs)



    ## method interfaces

    # add single channel
    f.add_channel("ch2", pids, data)

    # add multiple channels from one dict
    chans = {
        "ch3": (pids, data),
        "ch4": (pids, data)
    }
    f.add_channels(chans)

    # add multiple channels from two dicts
    many_pids = {
        "ch5": pids,
        "ch6": pids
    }
    many_data = {
        "ch5": data,
        "ch6": data
    }
    f.add_channels(many_pids, many_data)

    # add multiple channels via kwargs
    f.add_channels(ch7=(pids, data), ch8=(pids, data))


    # add single meta data entry
    f.add_meta_entry("m6", data)

    # add multiple meta data entries from dict
    entries = {
        "m7": data,
        "m8": data
    }
    f.add_meta_entries(entries)

    # add multiple meta data entries via kwargs
    f.add_meta_entries(m9=data, m10=data)



