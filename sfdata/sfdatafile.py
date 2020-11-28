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


class SFDataFile(FileContext, SFData):

    def __init__(self, fname):
        self.fname = fname
        self.file, channels = load_from_file(fname)
        super().__init__(channels)

    def close(self):
        self.file.close()

    def __repr__(self):
        tn = typename(self)
        fn = self.fname
        entries = len(self)
        return f"{tn}(\"{fn}\"): {entries} channels"



def load_from_file(fname):
    if ".JF" in fname: #TODO: might need better check
        if ju:
            return load_from_ju_file(fname)
        else:
            print("Warning: Could not import jungfrau_utils, will treat JF files as regular files.")

    return load_from_generic_file(fname)


def load_from_ju_file(fname):
    juf = ju.File(fname)
    name = juf.detector_name
    chan = SFChannelJF(name, juf)
    return juf, {name: chan}


def load_from_generic_file(fname):
    h5 = h5py.File(fname, mode="r")

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

    return h5, channels



