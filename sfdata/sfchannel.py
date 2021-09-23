from types import SimpleNamespace
import numpy as np

from .errors import DatasetNotInGroupError
from .utils import typename, adjust_shape, batched, apply_batched, ClosedH5


class SFChannel:

    def __init__(self, name, group):
        self.name = name
        self._group = group
        self.datasets = SimpleNamespace(
            data = get_dataset("data", group),
            pids = get_dataset("pulse_id", group)
        )
        self.offset = 0
        self.reset_valid()

    def close(self):
        self._group = ClosedH5(self._group)
        self.datasets.data = ClosedH5(self.datasets.data)
        self.datasets.pids = ClosedH5(self.datasets.pids)

    def in_batches(self, size=100, n=None):
        dataset = self.datasets.data
        valid_indices = self._get_valid_indices()
        return batched(dataset, valid_indices, size, nbatches=n)

    def apply_in_batches(self, func, size=100, n=None):
        dataset = self.datasets.data
        valid_indices = self._get_valid_indices()
        return apply_batched(func, dataset, valid_indices, size, nbatches=n)


    def __getitem__(self, key):
        if isinstance(key, tuple):
            key = list(key)
        else:
            key = [key]

        first = key[0]
        indices = self._get_valid_indices()
        key[0] = indices[first]

        key = tuple(key)
        res = self.datasets.data.__getitem__(key)
        return res


    @property
    def data(self):
        return self._get(self.datasets.data)

    @property
    def pids(self):
        return self._get(self.datasets.pids) - self.offset

    def _get(self, dataset):
        res = dataset[:][self.valid] #TODO: workaround: access from h5 via indices is slow
        res = adjust_shape(res)
        return res

    @property
    def dtype(self):
        return self.datasets.data.dtype

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def size(self):
        return np.prod(self.shape)

    @property
    def shape(self):
        first_dim = self.nvalid
        other_dims = self.datasets.data.shape[1:]
        shape = (first_dim, *other_dims)
        return shape

    @property
    def ntotal(self):
        return self.datasets.pids.shape[0]

    @property
    def nvalid(self):
        valid = self.valid
        if valid is Ellipsis:
            return self.ntotal
        else:
            return len(valid)

    def reset_valid(self):
        #TODO: check "is_data_present" for valid entries, initialize from these
        self.valid = Ellipsis

    def _get_valid_indices(self):
        valid = self.valid
        if valid is Ellipsis:
            valid = np.arange(self.ntotal)
        return valid

    def __repr__(self):
        tn = typename(self)
        name = self.name
        return f"{tn}: {name}"

    def __iter__(self):
        def gen():
            yield self.pids
            yield self.data
        return gen()



def get_dataset(name, group):
    try:
        res = group[name]
    except Exception as exc: #TODO: limit this to ValueError("Field names only allowed for compound types") ?
        raise DatasetNotInGroupError(name, group) from exc
    else:
        return res



