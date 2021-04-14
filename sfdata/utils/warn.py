from warnings import warn

from .utils import typename


def print_skip_warning(exc, name):
    excname = typename(exc)
    warn(f"Warning: Skipping {name} since it caused {excname}: {exc}", stacklevel=2)



