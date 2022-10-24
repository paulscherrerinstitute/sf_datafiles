
class ClosedH5:
    """
    This class allows to better handle closed h5 files:

    originally:
    - ch._group.name gives None
    - ch.datasets.data[...] / ch.datasets.pids[...] / shapes etc. raise ValueError: Not a dataset

    here:
    - any interaction with ch._group / ch.datasets.* (i.e., also ch.data or ch.shape) raises ClosedH5Error
    - error message contains helpful file name and group name
    - closing several times is possible, i.e., ClosedH5(ClosedH5(group)) -> ClosedH5(group)
    """

    def __init__(self, group):
        # the following allows to close a file several times without losing the names
        if isinstance(group, type(self)): # copy contents if group was closed before
            self.group = group.group
            self.fname = group.fname
            self.gname = group.gname
            return

        self.group = group

        try:
            gf = group.file # ID only valid while file is open
        except ValueError:  # "not an ID of a file object"
            fname = None
        else:
            fname = gf.filename

        self.fname = fname
        self.gname = group.name # is None if file is closed


    def __repr__(self):
        fname = format_name("file", self.fname)
        gname = format_name("group", self.gname)
        return f"Closed HDF5 {gname} from {fname}"


    def _raise_error(self, *args, **kwargs):
        raise ClosedH5Error(self.fname, self.gname)

    __getattr__ = __getitem__ = _raise_error



class ClosedH5Error(Exception):

    def __init__(self, fname, gname):
        fname = format_name("file", fname)
        gname = format_name("group", gname)
        super().__init__(f"{fname} containing {gname} is closed...\nDid you try to access data outside of a with statement or after a close()?")



def format_name(ntype, name):
    return f"{ntype} \"{name}\"" if name else f"unknown {ntype}"



