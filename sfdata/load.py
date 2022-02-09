from glob import iglob


def make_loader(instrument="*a", pgroup="p*", run="*"):
    def loader_wrapper(instrument=instrument, pgroup=pgroup, run=run, debug=False):
        return loader(instrument, pgroup, run, debug)
    return loader_wrapper



def loader(instrument, pgroup, run, debug):
    pgroup = harmonize(pgroup, "p", 5)
    run = harmonize(run, "run", 4)

    pattern = f"/sf/{instrument}/data/{pgroup}/raw/{run}"
    res = sorted(iglob(pattern))

    if debug:
        print(pattern, "-> #runs:", len(res))
        return pattern
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


    assert load(instrument="TEST") == "/sf/TEST/data/p*/raw/run*"
    assert load(pgroup="TEST") == "/sf/*a/data/pTEST/raw/run*"
    assert load(run="TEST") == "/sf/*a/data/p*/raw/runTEST"


    ref = "/sf/*a/data/p*/raw/run*"

    assert ref == load()
    assert ref == load(run="*")
    assert ref == load(run="run*")
    assert ref == load(pgroup="*")
    assert ref == load(pgroup="p*")


    ref = "/sf/*a/data/p*/raw/run0001"

    assert ref == load(run=1)
    assert ref == load(run="1")
    assert ref == load(run="01")
    assert ref == load(run="run1")
    assert ref == load(run="run00001")


    ref = "/sf/*a/data/p12345/raw/run*"

    assert ref == load(pgroup=12345)
    assert ref == load(pgroup="12345")
    assert ref == load(pgroup="p12345")



