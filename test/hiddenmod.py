import sys
import importlib


def hide_module(name):
    mod = importlib.import_module(name)
    mod_fname = mod.__file__

    ending = f"/{name}/__init__.py"
    assert mod_fname.endswith(ending)
    mod_folder = mod_fname[:-len(ending)]
    sys.path.remove(mod_folder)

#    del mod
    del sys.modules[name]



class HiddenModule:

    def __init__(self, name):
        self.name = name
        self.was_loaded = (name in sys.modules)

        self.mod = mod = importlib.import_module(name)
        mod_fname = mod.__file__

        ending = f"/{name}/__init__.py"
        assert mod_fname.endswith(ending)
        self.mod_folder = mod_folder = mod_fname[:-len(ending)]
        sys.path.remove(mod_folder)

        del sys.modules[name]


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.path.append(self.mod_folder)
        if self.was_loaded:
            sys.modules[self.name] = self.mod
        return (exc_type is None)





if __name__ == "__main__":
    with HiddenModule("jungfrau_utils"):
        try:
            import jungfrau_utils as ju
        except ImportError:
            print("worked")
        else:
            print("failed")

    assert sys.modules.get("jungfrau_utils") is None
    import jungfrau_utils as ju
    assert sys.modules.get("jungfrau_utils")

    with HiddenModule("jungfrau_utils"):
        try:
            import jungfrau_utils as ju
        except ImportError:
            print("worked")
        else:
            print("failed")

    assert sys.modules.get("jungfrau_utils")
    import jungfrau_utils as ju


    #hide_module("jungfrau_utils")

    #import jungfrau_utils as ju



