from types import SimpleNamespace
import numpy as np
from .utils import typename, adjust_shape, batcher, apply_to_batches


class SFChannel:

    def __init__(self, group):
        self._group = group
        self.datasets = SimpleNamespace(
            data = self._group["data"],
            pids = self._group["pulse_id"]
        )
        self.reset_valid()

    @property
    def name(self):
        return self._group.name.split("/")[-1]

    def in_batches(self, size=100):
        dataset = self.datasets.data
        valid = self.valid
        if valid is Ellipsis:
            valid = np.arange(self.nvalid)
        return batcher(dataset, valid, size)

    def apply_in_batches(self, func, size=100):
        batches = self.in_batches(size=size)
        return apply_to_batches(func, batches, self.nvalid)

    @property
    def data(self):
        data = self.datasets.data[:][self.valid] # TODO: workaround: access from h5 via indices is slow
        data = adjust_shape(data)
        return data

    @property
    def pids(self):
        return self.datasets.pids[:][self.valid] # TODO: workaround: access from h5 via indices is slow

    @property
    def shape(self):
        first_dim = self.nvalid
        other_dims = self.datasets.data.shape[1:]
        shape = (first_dim, *other_dims)
        return shape

    @property
    def nvalid(self):
        valid = self.valid
        if valid is not Ellipsis:
            return len(valid)
        else:
            return self.datasets.data.shape[0]

    def reset_valid(self):
        #TODO: check "is_data_present" for valid entries, initialize from these
        self.valid = Ellipsis

    def __repr__(self):
        tn = typename(self)
        name = self.name
        return f"{tn}: {name}"



#TODO: better handle closed h5 files:
#- _group.name gives None
#- datasets.data[...] / datasets.pids[...] / shapes raise ValueError: Not a dataset (not a dataset)



