import os
from glob import glob

from .sfdatafiles import SFDataFiles
from .utils import json_load


class SFRunInfo(SFDataFiles):

    def __init__(self, fname):
        self.fname = fname
        self.info = info = json_load(fname)

        directory = info["directory_name"]
        datafiles = get_datafiles(fname, directory)
        super().__init__(*datafiles)

        #TODO: which entries? variable names?
        self.instrument = info["beamline"]
        self.pgroup     = info["pgroup"]
        self.directory  = directory
        self.run_number = info["run_number"]

        # static data does not have the scan_info entry
        self.scan_step_info = info.get("scan_info")


    @property
    def is_scan_step(self):
        return self.scan_step_info is not None



def get_datafiles(fname, directory):
    raw = parents(fname, 2) # traverse upwards run_info/00?000/
    pattern = os.path.join(raw, directory, "*.h5")
    return glob(pattern)

def parents(fname, n):
    n += 1 # include the filename itself
    return repeat(n, os.path.dirname, fname)

def repeat(n, f, arg):
    for _ in range(n):
        arg = f(arg)
    return arg



##TODO: switch everything to pathlib?
#def get_datafiles(fname, directory):
#    fname = Path(fname)
#    folder = fname.parents[2] / directory
#    datafiles = folder.glob("*.h5")
#    datafiles = (str(df) for df in datafiles) # glob.glob (in explode_filenames()) does not accept pathlib.Path
#    return datafiles



