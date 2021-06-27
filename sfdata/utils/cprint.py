from colorama import Fore


COLORS = {
    "black":   Fore.BLACK,
    "red":     Fore.RED,
    "green":   Fore.GREEN,
    "yellow":  Fore.YELLOW,
    "blue":    Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan":    Fore.CYAN,
    "white":   Fore.WHITE,
    "reset":   Fore.RESET,
    None:      Fore.RESET
}


def ncprint(*objects, color=None, sep=" ", **kwargs):
    return cprint(*objects, color=None, sep=sep, **kwargs)

def cprint(*objects, color=None, sep=" ", **kwargs):
    color = get_color(color)
    text = flatten_strings(objects, sep)
    return _print(color, text, sep, kwargs)

def get_color(color):
    try:
        return COLORS[color]
    except KeyError as exc:
        color = repr(color)
        allowed = tuple(COLORS.keys())
        raise ValueError(f"{color} not from {allowed}") from exc

def flatten_strings(objects, sep):
    return sep.join(str(i) for i in objects)

def _print(color, text, sep, kwargs):
    return print(color + text + Fore.RESET, sep=sep, **kwargs)



