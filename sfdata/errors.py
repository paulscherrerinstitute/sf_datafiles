
class SFDataError(Exception):
    pass


class NoUsableFileError(SFDataError):

    def __init__(self):
        msg = "No entry contained a usable file"
        super().__init__(msg)


class NoMatchingFileError(SFDataError):

    def __init__(self, patterns, ftype=None):
        ftype = f"{ftype} " if ftype else ""
        msg = f"No matching {ftype}file for patterns: {patterns}"
        super().__init__(msg)


class NoUsableChannelError(SFDataError):

    def __init__(self, fname):
        msg = f"No usable channel in: {fname}"
        super().__init__(msg)


class DatasetNotInGroupError(SFDataError):

    def __init__(self, name, group):
        msg = f"Cannot get dataset \"{name}\" from: {group}"
        super().__init__(msg)


class ArrayLengthMismatch(SFDataError):

    def __init__(self, name, npids, ndata):
        msg = f"Cannot create channel \"{name}\" due to array length mismatch: #pids = {npids} vs. #data = {ndata}"
        super().__init__(msg)



