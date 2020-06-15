from .h5filewrapper import H5FileWrapper
from .sfdata import SFData
from .sfchannel import SFChannel


class SFDataFile(H5FileWrapper, SFData):

    def __init__(self, *args, **kwargs):
        H5FileWrapper.__init__(self, *args, **kwargs)
        channels = load_from_file(self.file)
        SFData.__init__(self, channels)



def load_from_file(h5):
    if "data" in h5:
        data = h5["data"] # some files have /data/, e.g., bsread
    else:
        data = h5 # some files do not, e.g., camera

    channels = {}
    for cn in data:
        c = data[cn]
        c = SFChannel(c)
        channels[cn] = c
    return channels



