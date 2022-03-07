import numpy as np
from .sfchannel import SFChannel


class SFChannelJF(SFChannel):

    def __init__(self, name, juf):
        self.juf = juf
        super().__init__(name, juf)
        self.datasets.data = juf # replace raw dataset with ju.File object

    @classmethod
    def from_file(cls, juf):
        name = juf.detector_name
        return cls(name, juf)

    @property
    def shape(self):
        nimages = self.nvalid
        juf = self.juf
        image_shape = juf.handler.get_shape_out(gap_pixels=juf.gap_pixels, geometry=juf.geometry)
        shape = (nimages, *image_shape)
        return shape

    def reset_valid(self):
        self.valid = Ellipsis
        # load "is_good_frame", check for any invalid entries, initialize from it
        good = self.juf.file.get(f"data/{self.name}/is_good_frame")
        if good is None:
            return
        good = good[:]
        if good.all():
            return
        good = good.reshape(-1).nonzero()[0] # nonzero returns a tuple of arrays, one for each dimension also for 1D
        self.valid = good



