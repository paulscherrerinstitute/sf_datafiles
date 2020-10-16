
def strlen(val):
    return len(str(val))

def maxstrlen(iterable):
    return max(strlen(i) for i in iterable)


def print_line(length=80, char="-"):
    print("\n" + char*length + "\n")


def printable_string_sequence(strings):
    strings = (nice_string_repr(s) for s in strings)
    return ", ".join(strings)

def nice_string_repr(string):
    return repr(string).replace("'", '"')



