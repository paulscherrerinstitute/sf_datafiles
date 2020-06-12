from types import SimpleNamespace
from .utils import typename


class SFChannel:

    def __init__(self, group):
        self._group = group
        self.datasets = SimpleNamespace(
            data = self._group["data"],
            pids = self._group["pulse_id"]
        )

    @property
    def name(self):
        base = self._group.parent.name + "/"
        name = self._group.name
        return name[len(base):]

    @property
    def data(self):
        data = self.datasets.data[:]
        if data.ndim == 2 and data.shape[1] == 1:
            return data.reshape(-1)
        return data

    @property
    def pids(self):
        return self.datasets.pids[:]

    @property
    def shape(self):
        return self.datasets.data.shape

    def __repr__(self):
        tn = typename(self)
        name = self.name
        return f"{tn}: {name}"



#TODO: check "is_data_present" for valid entries, return only those
