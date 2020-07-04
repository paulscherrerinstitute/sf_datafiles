from glob import glob

from .filecontext import FileContext
from .utils import typename, printable_string_sequence
from .sfdata import SFData
from .sfdatafile import SFDataFile


class SFDataFiles(FileContext, SFData):

    def __init__(self, *patterns):
        self.fnames = fnames = explode_filenames(patterns)
        if not fnames:
            patterns = printable_string_sequence(patterns)
            raise ValueError(f"No matching file for patterns: {patterns}")
        self.files = [SFDataFile(fn) for fn in fnames]
        super().__init__()
        for f in self.files:
            self.update(f)

    def close(self):
        for f in self.files:
            f.close()

    def __repr__(self):
        tn = typename(self)
        fns = self.fnames
        fns = "\", \"".join(fns)
        entries = len(self)
        return f"{tn}(\"{fns}\"): {entries} channels"



def explode_filenames(patterns):
    fnames = []
    for p in patterns:
        fns = glob(p)
        fnames.extend(fns)
    fnames = sorted(set(fnames))
    return fnames



