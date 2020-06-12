import h5py

from .utils import typename


class H5FileWrapper:

    #TODO: h5py 3.0 will change the default mode to "r". Once this is widely available we can remove our changed default here.
    def __init__(self, fname, *args, mode="r", **kwargs):
        self.fname = fname
        self.file = h5py.File(fname, *args, mode=mode, **kwargs)

    def __repr__(self):
        tn = typename(self)
        fn = self.fname
        return f"{tn}(\"{fn}\")"

    def __enter__(self):
#        print("enter")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
#        print("exit({}, {}, {})".format(exc_type, repr(exc_value), exc_traceback))
        self.close()
        return (exc_type is None)

    def close(self):
        self.file.close()



