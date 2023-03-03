from collections import UserDict
import functools
import h5py

from .utils import ClosedH5, typename


cached = functools.lru_cache(maxsize=None)


class SFMeta(UserDict):

    @property
    def names(self):
        return tuple(self.keys())

    @property
    def entries(self):
        return tuple(self.values())


    def __init__(self, *args, **kwargs):
        # SFMeta is supposed to be read-only, but the UserDict constructor uses __setitem__
        # the following flag controls whether this is allowed or not
        self._initialized = False
        super().__init__(*args, **kwargs)
        self._initialized = True

        # create a cached version of getitem here so that it is per object and not per class
        # allows to clear the cache (via close) per object
        # does not need self as argument, thus does not trigger the following problem:
        #   dict defines __eq__ (which invalidates the default __hash__ to maintain consistency)
        #   but not __hash__ due to being mutable
        #   lru_cache expects hashable function arguments, which self would not be
        super_getitem = super().__getitem__
        @cached
        def _getitem(key):
            return super_getitem(key)[()]
        self._getitem = _getitem


    def __getitem__(self, key):
        return self._getitem(key)

    def __setitem__(self, key, value):
        if self._initialized:
            tn = typename(self)
            raise TypeError(f"'{tn}' object does not support item assignment")
        else:
            return super().__setitem__(key, value)

    def __delitem__(self, key):
        tn = typename(self)
        raise TypeError(f"'{tn}' object doesn't support item deletion")


    # ipython cannot tab complete UserDict keys without this
    def _ipython_key_completions_(self):
        return self.keys()


    def close(self):
        # replace entries with ClosedH5
        #TODO: is the isinstance check needed?
        closed = {
            k: ClosedH5(v) if isinstance(v, h5py.Dataset) else v
            for k, v in self.items()
        }
        self.update(closed)
        # clear the getitem cache to avoid memory leaks
        self._getitem.cache_clear()

    def __repr__(self):
        tn = typename(self)
        entries = len(self)
        return f"{tn}: {entries} entries"



def get_meta(group, name="meta"):
    try:
        meta = group[name]
    except KeyError:
        #TODO: warning?
        #TODO: return empty SFMeta object?
        return None
    else:
        return SFMeta(meta)



