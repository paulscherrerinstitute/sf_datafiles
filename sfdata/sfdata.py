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
        pids = set()
        for chan in self.channels.values():
            pids |= set(chan.pids)
        return np.array(sorted(pids))

    def to_dataframe(self, show_progress=False):
        df = pd.DataFrame(index=self.pids, columns=self.names, dtype=object) # object dtype makes sure NaN can be used as missing marker also for int/bool
        channels = self.channels.values()
        if show_progress:
            channels = tqdm(channels)
        for chan in channels:
            which = np.isin(self.pids, chan.pids)
            df[chan.name][which] = chan.data[:]
        return df

    def __len__(self):
        return len(self.channels)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            chans = {k: self.channels[k] for k in key}
            return SFData(chans)
        return self.channels[key]

    def __repr__(self):
        tn = typename(self)
        entries = len(self)
        return f"{tn}: {entries} channels"
#        return repr(self.channels)



