import functools

from .utils import typename


class SFMeta(dict):

    names = property(dict.keys)
    entries = property(dict.values)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create a cached version of getitem here so that it is per object and not per class
        # allows to clear the cache (via close) per object
        # does not need self as argument, thus does not trigger the following problem:
        #   dict defines __eq__ (which invalidates the default __hash__ to maintain consistency)
        #   but not __hash__ due to being mutable
        #   lru_cache expects hashable function arguments, which self would not be
        getitem = super().__getitem__
        @functools.lru_cache(maxsize=None)
        def _getitem(key):
            return getitem(key)[:]
        self._getitem = _getitem


    def __getitem__(self, key):
        return self._getitem(key)

    def close(self):
        #TODO replace entries with ClosedH5
        self._getitem.cache_clear() # clear the getitem cache to avoid memory leaks

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



