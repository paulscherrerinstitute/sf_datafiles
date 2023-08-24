from warnings import warn

import h5py
import bitshuffle.h5

from .errors import NoUsableChannelError
from .utils import typename, enquote, print_skip_warning, FileContext, FileStatus
from .sfdata import SFData
from .sfchannel import SFChannel
from .sfchanneljf import SFChannelJF
from .sfmeta import get_meta

#TODO: treat ju as optional for now
try:
    import jungfrau_utils as ju
except ImportError:
    ju = None


NAME_FILE_META = "general"
NAME_FILE_DATA_ROOT = "data"


class SFDataFile(FileContext, SFData):

    def __init__(self, fname):
        self.fname = fname
        self.fs = FileStatus(fname)
        self.file, channels = load_from_file(fname)
        self.meta = get_meta(self.file, NAME_FILE_META)
        super().__init__(channels)

    def close(self):
        # channels and meta should be closed before the underlying file such that file name and group name still exist and can be used in error messages
        for ch in self.channels:
            ch.close()
        if self.meta:
            self.meta.close()
        self.file.close()

    def __repr__(self):
        tn = typename(self)
        fn = enquote(self.fname)
        entries = len(self)
        return f"{tn}({fn}): {entries} channels"



def load_from_file(fname):
    if ".JF" in fname: #TODO: might need better check
        if ju:
            return load_from_ju_file(fname)
        else:
            warn("Could not import jungfrau_utils, will treat JF files as regular files.", stacklevel=2)

    return load_from_generic_file(fname)


def load_from_ju_file(fname):
    with h5py.File(fname) as f:
        names = f["data"].keys()
        names = sorted(names)

    if len(names) == 1:
        return load_from_ju_file_single_channel(fname)
    else:
        return load_from_ju_file_multiple_channels(fname, names)


def load_from_ju_file_single_channel(fname):
    juf = ju.File(fname)
    name = juf.detector_name
    chan = SFChannelJF(name, juf)
    return juf, {name: chan}


def load_from_ju_file_multiple_channels(fname, names):
    fdemux = FileDemultiplexer()
    chans = {}
    for n in names:
        juf = ju.File(fname, detector_name=n)
        chan = SFChannelJF(n, juf)
        fdemux.add(juf)
        chans[n] = chan
    return fdemux, chans


class FileDemultiplexer(set):

    def close(self):
        for f in self:
            f.close()


def load_from_generic_file(fname):
    h5 = h5py.File(fname, mode="r")

    if NAME_FILE_DATA_ROOT in h5:
        data = h5[NAME_FILE_DATA_ROOT] # some files have /data/, e.g., bsread
    else:
        data = h5 # some files do not, e.g., camera

    channels = {}
    for name in data:
        if name == NAME_FILE_META: # skip the file meta data group
            continue
        group = data[name]
        try:
            chan = SFChannel(name, group)
        except Exception as exc:
            cn = enquote(name)
            cn = f"channel {cn}"
            print_skip_warning(exc, cn)
        else:
            channels[name] = chan

    if not channels:
        raise NoUsableChannelError(fname)

    return h5, channels



