import h5py
import bitshuffle.h5

from .filecontext import FileContext
from .utils import typename
from .sfdata import SFData
from .sfchannel import SFChannel
from .sfchanneljf import SFChannelJF

#TODO: treat ju as optional for now
try:
    import jungfrau_utils as ju
except ImportError:
    ju = None
    print("Warning: Could not import jungfrau_utils, will treat JF files as regular files.")


class SFDataFile(FileContext, SFData):

    def __init__(self, fname):
        self.fname = fname

        if ju and ".JF" in fname: #TODO: might need better check
            self.file = ju.File(fname)
            channels = load_from_ju_file(self.file)
        else:
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



def load_from_ju_file(juf):
    name = juf.detector_name
    chan = SFChannelJF(name, juf)
    return {name: chan}



def load_from_file(h5):
    if "data" in h5:
        data = h5["data"] # some files have /data/, e.g., bsread
    else:
        data = h5 # some files do not, e.g., camera

    channels = {}
    for name in data:
        if name == "pulse_id": #TODO: workaround for a spurious pulse_id group in bsread files
            continue
        chan = data[name]
        chan = SFChannel(name, chan)
        channels[name] = chan
    return channels



