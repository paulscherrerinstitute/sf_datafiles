from .utils import adjust_shape, json_load


class SFScanInfo:

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



