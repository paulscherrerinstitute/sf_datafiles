import h5py

from .errors import ArrayLengthMismatch
from .utils import typename, enquote, FileContext, FileStatus
from .sfdata import SFData
from .sfchannel import SFChannel

from .sfdatafile import NAME_FILE_META, NAME_FILE_DATA_ROOT
from .sfchannel import NAME_CHAN_DATA, NAME_CHAN_PIDS, NAME_CHAN_TIMESTAMPS, NAME_CHAN_META


ALLOWED_MODES = ("w", "w-", "x")


class SFProcFile(FileContext, SFData):

    def __init__(self, fname, *args, mode="x", **kwargs):
        if mode not in ALLOWED_MODES:
            allowed = ", ".join(ALLOWED_MODES)
            raise ValueError(f"Invalid mode; must be one of {allowed}")

        super().__init__()
        self.fname = fname
        self.fs = FileStatus(fname)
        self.file = h5py.File(fname, *args, mode=mode, **kwargs)
        self._data = None
        self._meta = None


    @property
    def data(self):
        if self._data is None:
            self._data = self.file.create_group(NAME_FILE_DATA_ROOT)
        return self._data

    @property
    def meta(self):
        if self._meta is None:
            self._meta = self.file.create_group(NAME_FILE_META)
        return self._meta

    @property
    def attrs(self):
        return self.file.attrs

    def close(self):
        self.file.close()

    def __repr__(self):
        tn = typename(self)
        fn = enquote(self.fname)
        entries = len(self)
        return f"{tn}({fn}): {entries} channels"

    def __len__(self):
        data = self._data
        if data is None:
            return 0
        return len(data)


    def __getitem__(self, name):
        data = self._data
        if data is None:
            msg = f"Unable to open object (object '{name}' doesn't exist)"
            raise KeyError(msg)

        chan = data[name] #TODO: should this be dict.__getitem__(self, name) ?
        return SFChannel(name, chan)


    def __setitem__(self, name, value):
        self.add_channel(name, *value)


    def drop_missing(self):
        tn = typename(self)
        raise NotImplementedError(f"cannot drop missing on {tn}")


    def add_channel(self, name, pids, data):
        npids = len(pids)
        ndata = len(data)
        if npids != ndata:
            raise ArrayLengthMismatch(name, npids, ndata)

        group = self.data.create_group(name)
        group.create_dataset(NAME_CHAN_PIDS, data=pids)
        group.create_dataset(NAME_CHAN_DATA, data=data)

        chan = SFChannel(name, group)
        super().__setitem__(name, chan)
        return chan


    def add_channels(self, *args, **kwargs):
        """
        accepts either
        - one dict:  {name: (pids, data), ...}
        - two dicts: {name: pids, ...}, {name: data, ...}
        - n kwargs:  name=(pids, data), ...
        """
        channels = parse_2_args("add_channels", args, kwargs)
        for name, values in channels.items():
            self.add_channel(name, *values)


    def add_meta_entry(self, name, value):
        return self.meta.create_dataset(name, data=value)


    def add_meta_entries(self, *args, **kwargs):
        """
        accepts either
        - one dict: {name: value, ...}
        - n kwargs: name=value, ...
        """
        entries = parse_1_args("add_meta_entries", args, kwargs)
        for name, value in entries.items():
            self.add_meta_entry(name, value)





def parse_1_args(funcname, args, kwargs):
    nargs = len(args)
    if nargs == 0:
        res = {}
    elif nargs == 1:
        res = args[0]
    else:
        raise TypeError(f"{funcname}() takes either zero or one arguments but {nargs} were given")

    res.update(kwargs)
    return res


def parse_2_args(funcname, args, kwargs):
    nargs = len(args)
    if nargs == 0:
        res = {}
    elif nargs == 1:
        res = args[0]
    elif nargs == 2:
        res = stack_dicts(*args)
    else:
        raise TypeError(f"{funcname}() takes either zero, one or two positional arguments but {nargs} were given")

    res.update(kwargs)
    return res


def stack_dicts(a, b):
    ka = a.keys()
    kb = b.keys()
    if ka != kb:
        symdiff = sorted(ka ^ kb)
        msg = f"cannot stack dictionaries due to differing keys: {symdiff}"
        raise KeyError(msg)

    return {n: (a[n], b[n]) for n in a}



#TODO:
#- add SFProcFile.update() !
#- add SFProcFile.add_attribute() / .add_attributes() for consistency?
#- allow mode="a" ?
#  would need to read file's existing channels
#- allow appending/changing ch.pids/ch.data ?
#  would need different SFChannel
#  how to assert same length?



