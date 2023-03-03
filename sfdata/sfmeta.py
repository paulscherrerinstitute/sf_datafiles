from collections.abc import Mapping
import functools
import h5py

from .utils import ClosedH5, typename


cached = functools.lru_cache(maxsize=None)


class SFMeta(Mapping):

    @property
    def names(self):
        return tuple(self.keys())

    @property
    def entries(self):
        return tuple(self.values())


    def __init__(self, group):
        super().__init__()
        self._group = group

        # create a cached version of getitem here so that it is per object and not per class
        # allows to clear the cache (via close) per object
        # does not need self as argument, thus does not trigger the following problem:
        #   dict defines __eq__ (which invalidates the default __hash__ to maintain consistency)
        #   but not __hash__ due to being mutable
        #   lru_cache expects hashable function arguments, which self would not be
        @cached
        def _getitem(key):
            return self._group[key][()]
        self._getitem = _getitem


    def __getitem__(self, key):
        return self._getitem(key)

    def close(self):
        # replace entries with ClosedH5
        #TODO: is the isinstance check needed?
        self._group = {
            k: ClosedH5(v) if isinstance(v, h5py.Dataset) else v
            for k, v in self._group.items()
        }
        # clear the getitem cache to avoid memory leaks
        self._getitem.cache_clear()

    def __iter__(self):
        return iter(self._group)

    def __len__(self):
        return len(self._group)

    def __repr__(self):
        tn = typename(self)
        entries = len(self)
        return f"{tn}: {entries} entries"

    # ipython cannot tab complete Mapping keys without this
    def _ipython_key_completions_(self):
        return self.keys()



def get_meta(group, name="meta"):
    try:
        meta = group[name]
    except KeyError:
        #TODO: warning?
        #TODO: return empty SFMeta object?
        return None
    else:
        return SFMeta(meta)



