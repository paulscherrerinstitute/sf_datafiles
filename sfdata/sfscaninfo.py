from collections.abc import Sequence
from .errors import NoMatchingFileError, NoUsableFileError
from .utils import adjust_shape, json_load, typename
from .sfdatafiles import SFDataFiles


class SFScanInfo(Sequence):

    def __init__(self, fname):
        self.fname = fname
        self.data = data = json_load(fname)

        self.files = files = data["scan_files"]
        self.parameters    = data["scan_parameters"]

        values    = data["scan_values"]
        readbacks = data["scan_readbacks"]

        values    = adjust_shape(values)
        readbacks = adjust_shape(readbacks)

        self.values     = values
        self.readbacks  = readbacks


    def __iter__(self):
#        return (SFDataFiles(*fns) for fns in self.files) #TODO: errors stop the iteration. do we want this?
        return generate_sfdata(self.files)

    def __getitem__(self, index):
        fns = self.files[index]
        return SFDataFiles(*fns)

    def __len__(self):
        return len(self.files)


    def __repr__(self):
        tn = typename(self)
        fn = self.fname
        nsteps = len(self)
        return f"{tn}(\"{fn}\"): {nsteps} steps"



def generate_sfdata(fnames):
    nothing_opened = True
    for i, fns in enumerate(fnames):
        try:
            yield SFDataFiles(*fns)
            nothing_opened = False
        except NoMatchingFileError as exc:
            print_skip_warning(exc, i)
        except Exception as exc:
            sn = f"{i} {fns}"
            print_skip_warning(exc, sn)
    if nothing_opened:
        raise NoUsableFileError("No entry contained a usable file")


def print_skip_warning(exc, step_name):
    excname = typename(exc)
    print(f"Warning: Skipping step {step_name} since it caused {excname}: {exc}")



