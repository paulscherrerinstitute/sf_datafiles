import h5py

from .utils import typename


class H5FileWrapper:

    def __init__(self, fname, *args, **kwargs):
        self.fname = fname
        self.file = h5py.File(fname, *args, **kwargs)

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



