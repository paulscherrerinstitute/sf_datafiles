from .h5filewrapper import H5FileWrapper
from .sfdata import SFData
from .sfchannel import SFChannel


class SFDataFile(H5FileWrapper, SFData):

    def __init__(self, *args, **kwargs):
        H5FileWrapper.__init__(self, *args, **kwargs)
        channels = load_from_file(self.file)
        SFData.__init__(self, channels)



def load_from_file(h5):
    channels = {}

    #TODO: better way of doing this?
    if "data" in h5:
        data = h5["data"]
    else:
        data = h5

    for cn in data:
        c = data[cn]
        c = SFChannel(c)
        channels[cn] = c
    return channels



