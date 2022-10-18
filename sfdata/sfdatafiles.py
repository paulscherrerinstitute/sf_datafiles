from glob import glob
from warnings import warn

from .errors import NoMatchingFileError
from .utils import typename, enquote, printable_string_sequence, print_skip_warning, FileContext
from .sfdata import SFData
from .sfdatafile import SFDataFile
from .ign import remove_ignored_filetypes_run


class SFDataFiles(FileContext, SFData):

    def __init__(self, *patterns):
        super().__init__()
        self.fnames = []
        self.files = []
        self.load(*patterns)


    def close(self):
        for f in self.files:
            f.close()
        #TODO: clear self.fnames/self.files or remove individual closed files?

    def __repr__(self):
        tn = typename(self)
        fns = self.fnames
        fns = printable_string_sequence(fns)
        entries = len(self)
        return f"{tn}({fns}): {entries} channels"


    def load(self, *patterns): #TODO: check if fnames/file already in self.fnames/self.files?
        fnames = explode_filenames(patterns)
        fnames, files = load_files(fnames)

        if not files:
            patterns = printable_string_sequence(patterns)
            raise NoMatchingFileError(patterns)

        for f in files:
            self.update(f)

        self.fnames.extend(fnames)
        self.files.extend(files)



def explode_filenames(patterns):
    fnames = []
    for p in patterns:
        fns = glob(p)
        fnames.extend(fns)
    fnames = sorted(set(fnames))
    return fnames


def load_files(fnames):
    fnames = remove_ignored_filetypes_run(fnames)
    res = {}
    for fn in fnames:
        try:
            f = SFDataFile(fn)
        except Exception as exc:
            quoted_fn = enquote(fn)
            print_skip_warning(exc, quoted_fn)
        else:
            warn_masked_channels(fn, f, res)
            res[fn] = f

    fnames, files = dict_to_tuples(res)
    return fnames, files


def dict_to_tuples(d):
    keys   = d.keys()
    values = d.values()
    return tuple(keys), tuple(values)


def warn_masked_channels(new_fn, new_f, collected):
    for fn, f in collected.items():
        overlap = new_f.keys() & f.keys()
        if overlap:
            overlap = sorted(overlap)
            warn(f"The following channels from {fn} are masked by channels from {new_fn}: {overlap}", stacklevel=2)



