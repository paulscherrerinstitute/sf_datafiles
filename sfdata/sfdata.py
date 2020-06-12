from functools import reduce
import numpy as np
import pandas as pd
from tqdm import tqdm

from .utils import typename


class SFData:

    def __init__(self, channels):
        self.channels = channels

    def keys(self):
        return self.channels.keys()

    names = property(keys)

    def save_names(self, fname, mode="x", **kwargs):
        with open(fname, mode=mode, **kwargs) as f:
            data = "\n".join(self.names)
            data += "\n" * 2
            f.writelines(data)

    @property
    def pids(self):
        iter_pids = (c.pids for c in self.channels.values())
        return reduce(np.intersect1d, iter_pids)

    @property
    def all_pids(self):
        iter_pids = (c.pids for c in self.channels.values())
        return reduce(np.union1d, iter_pids)

    def to_dataframe(self, show_progress=False):
        all_pids = self.all_pids
        df = pd.DataFrame(index=all_pids, columns=self.names, dtype=object) # object dtype makes sure NaN can be used as missing marker also for int/bool
        channels = self.channels.values()
        if show_progress:
            channels = tqdm(channels)
        for chan in channels:
            which = np.isin(all_pids, chan.pids)
            df[chan.name].loc[which] = chan.datasets.data[:].tolist() # TODO: workaround for pandas not dealing with ndim. columns
        return df

    def __len__(self):
        return len(self.channels)

    def __getitem__(self, key):
        if isinstance(key, tuple) or isinstance(key, list): #TODO: decide for which types exactly
            chans = {k: self.channels[k] for k in key}
            return SFData(chans)
        return self.channels[key]

    def __repr__(self):
        tn = typename(self)
        entries = len(self)
        return f"{tn}: {entries} channels"
#        return repr(self.channels)



