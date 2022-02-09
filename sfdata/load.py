import collections
import itertools
from glob import iglob


def make_loader(instrument="*a", pgroup="p*", run="*"):
    def loader_wrapper(instrument=instrument, pgroup=pgroup, run=run, debug=False):
        return list(load_many(instrument, pgroup, run, debug))
    return loader_wrapper



def load_many(instrument, pgroup, run, debug):
    for i, p, r in product(instrument, pgroup, run):
        yield from load_one(i, p, r, debug)



def product(*vals):
    vals = ensure_seqs(*vals)
    return itertools.product(*vals)

def ensure_seqs(*vals):
    return (ensure_seq(i) for i in vals)

def ensure_seq(val):
    if isiterable(val):
        return val
    return (val,)

def isiterable(val):
    return isinstance(val, collections.abc.Iterable) and not isinstance(val, str)



def load_one(instrument, pgroup, run, debug):
    pgroup = harmonize(pgroup, "p", 5)
    run = harmonize(run, "run", 4)

    pattern = f"/sf/{instrument}/data/{pgroup}/raw/{run}"
    res = sorted(iglob(pattern))

    if debug:
        print(pattern, "-> #runs:", len(res))
        return [pattern]
    else:
        return res



def harmonize(val, prefix, nints):
    val = str(val)
    val = strip_prefix(val, prefix)
    val = pad_if_int(val, nints)
    val = prefix + val
    return val


def strip_prefix(string, prefix):
    if string.startswith(prefix):
        n = len(prefix)
        string = string[n:]
    return string


def pad_if_int(val, length):
    try:
        val = int(val)
    except ValueError:
        pass
    else:
        val = str(val)
        val = val.zfill(4)
    return val





# create a default load
load = make_loader()





if __name__ == "__main__":
    from functools import partial


    load = partial(load, debug=True)


    assert load(instrument="TEST") == ["/sf/TEST/data/p*/raw/run*"]
    assert load(pgroup="TEST")     == ["/sf/*a/data/pTEST/raw/run*"]
    assert load(run="TEST")        == ["/sf/*a/data/p*/raw/runTEST"]


    ref = ["/sf/*a/data/p*/raw/run*"]

    assert ref == load()
    assert ref == load(run="*")
    assert ref == load(run="run*")
    assert ref == load(pgroup="*")
    assert ref == load(pgroup="p*")


    ref = ["/sf/*a/data/p*/raw/run0001"]

    assert ref == load(run=1)
    assert ref == load(run="1")
    assert ref == load(run="01")
    assert ref == load(run="run1")
    assert ref == load(run="run00001")


    ref = ["/sf/*a/data/p12345/raw/run*"]

    assert ref == load(pgroup=12345)
    assert ref == load(pgroup="12345")
    assert ref == load(pgroup="p12345")


    ref = [
        "/sf/*a/data/p*/raw/run0010",
        "/sf/*a/data/p*/raw/run0020"
    ]

    assert ref == load(run=[10, 20])
    assert ref == load(run=iter(range(10, 20+10, 10)))



