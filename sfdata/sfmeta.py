import functools

from .utils import typename


class SFMeta(dict):

    names = property(dict.keys)

    # dict defines __eq__ (which invalidates the default __hash__ to maintain consistency)
    # but not __hash__ due to being mutable
    # lru_cache expects hashable function arguments, which self would not be
    # thus re-instantiate the original __hash__
    __hash__ = object.__hash__

    @functools.lru_cache(maxsize=None)
    def __getitem__(self, key):
        return super().__getitem__(key)[:]

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



