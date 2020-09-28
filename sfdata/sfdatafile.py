import h5py
import bitshuffle.h5

from .filecontext import FileContext
from .utils import typename
from .sfdata import SFData
from .sfchannel import SFChannel


class SFDataFile(FileContext, SFData):

    def __init__(self, fname):
        self.fname = fname
        self.file = h5py.File(fname, mode="r")
        channels = load_from_file(self.file)
        super().__init__(channels)

    def close(self):
        self.file.close()

    def __repr__(self):
        tn = typename(self)
        fn = self.fname
        entries = len(self)
        return f"{tn}(\"{fn}\"): {entries} channels"



def load_from_file(h5):
    if "data" in h5:
        data = h5["data"] # some files have /data/, e.g., bsread
    else:
        data = h5 # some files do not, e.g., camera

    channels = {}
    for cn in data:
        if cn == "pulse_id": #TODO: workaround for a spurious pulse_id group in bsread files
            continue
        c = data[cn]
        c = SFChannel(c)
        channels[cn] = c
    return channels



