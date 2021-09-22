from glob import glob

from .errors import NoMatchingFileError
from .utils import typename, printable_string_sequence, FileContext, enquote, print_skip_warning
from .sfdata import SFData
from .sfdatafile import SFDataFile
from .ign import remove_ignored_filetypes_run


class SFDataFiles(FileContext, SFData):

    def __init__(self, *patterns):
        fnames = explode_filenames(patterns)
        fnames, files = load_files(fnames)

        if not files:
            patterns = printable_string_sequence(patterns)
            raise NoMatchingFileError(patterns)

        self.fnames = fnames
        self.files = files

        super().__init__()
        for f in files:
            self.update(f)


    def close(self):
        for f in self.files:
            f.close()

    def __repr__(self):
        tn = typename(self)
        fns = self.fnames
        fns = printable_string_sequence(fns)
        entries = len(self)
        return f"{tn}({fns}): {entries} channels"



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
            res[fn] = f
    fnames, files = dict_to_tuples(res)
    return fnames, files


def dict_to_tuples(d):
    keys   = d.keys()
    values = d.values()
    return tuple(keys), tuple(values)



