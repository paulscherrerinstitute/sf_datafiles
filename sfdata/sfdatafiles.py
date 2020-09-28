from glob import glob

from .filecontext import FileContext
from .utils import typename, printable_string_sequence
from .sfdata import SFData
from .sfdatafile import SFDataFile


class SFDataFiles(FileContext, SFData):

    def __init__(self, *patterns):
        self.fnames = fnames = explode_filenames(patterns)
        self.files = files = load_files(fnames)

        if not files:
            patterns = printable_string_sequence(patterns)
            raise ValueError(f"No matching file for patterns: {patterns}")

        super().__init__()
        for f in files:
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


def load_files(fnames):
    files = []
    for fn in fnames:
        try:
            f = SFDataFile(fn)
        except Exception as exc:
            excname = typename(exc)
            print(f"Warning: Skipping \"{fn}\" since it caused {excname}: {exc}")
        else:
            files.append(f)
    return files



