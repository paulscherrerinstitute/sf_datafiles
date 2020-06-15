from functools import reduce
import numpy as np
import pandas as pd
from tqdm import tqdm

from .utils import typename


class SFData(dict):

    names = property(dict.keys)
    channels = property(dict.values)

    @property
    def pids(self):
        return reduce(np.intersect1d, self._iter_pids())

    @property
    def all_pids(self):
        return reduce(np.union1d, self._iter_pids())

    def _iter_pids(self):
        return (c.pids for c in self.values())

    def to_dataframe(self, show_progress=False):
        all_pids = self.all_pids
        df = pd.DataFrame(index=all_pids, columns=self.names, dtype=object) # object dtype makes sure NaN can be used as missing marker also for int/bool
        channels = self.values()
        if show_progress:
            channels = tqdm(channels)
        for chan in channels:
            which = np.isin(all_pids, chan.pids)
            df[chan.name].loc[which] = chan.datasets.data[chan.valid].tolist() # TODO: workaround for pandas not dealing with ndim. columns
        return df

    def drop_missing(self, show_progress=False):
        target_pids = self.pids
        channels = self.values()
        if show_progress:
            channels = tqdm(channels)
        for chan in channels:
            chan.reset_valid()
            _inters, ind_chan, _ind_target = np.intersect1d(chan.pids, target_pids, assume_unique=True, return_indices=True)
            chan.valid = ind_chan

    def reset_valid(self):
        channels = self.values()
        for chan in channels:
            chan.reset_valid()

    def save_names(self, fname, mode="x", **kwargs):
        with open(fname, mode=mode, **kwargs) as f:
            data = "\n".join(self.names)
            data += "\n" * 2
            f.writelines(data)

    def __getitem__(self, key):
        super_getitem = super().__getitem__
        if isinstance(key, (list, tuple)): #TODO: decide for which types exactly
            chans = {k: super_getitem(k) for k in key}
            return SFData(chans)
        return super_getitem(key)

    def __repr__(self):
        tn = typename(self)
        entries = len(self)
        return f"{tn}: {entries} channels"



