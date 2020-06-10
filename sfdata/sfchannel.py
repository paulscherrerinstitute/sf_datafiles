from .utils import typename


class SFChannel:

    def __init__(self, group):
        self._group = group

    @property
    def name(self):
        base = self._group.parent.name + "/"
        name = self._group.name
        return name[len(base):]

    @property
    def data(self):
        return self._group["data"]

    @property
    def pids(self):
        return self._group["pulse_id"]

    @property
    def shape(self):
        return self.data.shape

    def __repr__(self):
        tn = typename(self)
        name = self.name
        return f"{tn}: {name}"



#TODO: check "is_data_present" for valid entries, return only those
