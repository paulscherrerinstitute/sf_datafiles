from types import SimpleNamespace
from .utils import typename


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

    @property
    def data(self):
        data = self.datasets.data[self.valid]
        if data.ndim == 2 and data.shape[1] == 1: # transpose 1D column vectors to line vectors
            data = data.reshape(-1)
        return data

    @property
    def pids(self):
        return self.datasets.pids[self.valid]

    @property
    def shape(self):
        return self.datasets.data.shape

    def reset_valid(self):
        #TODO: check "is_data_present" for valid entries, initialize from these
        self.valid = Ellipsis

    def __repr__(self):
        tn = typename(self)
        name = self.name
        return f"{tn}: {name}"



