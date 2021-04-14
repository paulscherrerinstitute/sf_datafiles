from .utils import typename


def print_skip_warning(exc, name):
    excname = typename(exc)
    print(f"Warning: Skipping {name} since it caused {excname}: {exc}")



