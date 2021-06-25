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



