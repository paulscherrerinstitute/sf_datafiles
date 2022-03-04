import numpy as np
from .sfchannel import SFChannel


class SFChannelJF(SFChannel):

    def __init__(self, name, group):
        super().__init__(name, group)
        self.datasets.data = group # replace dataset with ju.File object

    @property
    def shape(self):
        nimages = self.nvalid
        juf = self._group
        image_shape = juf.handler.get_shape_out(gap_pixels=juf.gap_pixels, geometry=juf.geometry)
        shape = (nimages, *image_shape)
        return shape

    def reset_valid(self):
        self.valid = Ellipsis
        # load "is_good_frame", check for any invalid entries, initialize from it
        good = self._group.file.get(f"data/{self.name}/is_good_frame")
        if good is None:
            return
        good = good[:]
        if good.all():
            return
        good = good.reshape(-1).astype(bool)
        good = np.where(good)[0]
        self.valid = good



