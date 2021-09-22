from warnings import warn


IGNORED_FILETYPES = ["PVCHANNELS"]
PRINTABLE_IGNORED_FILETYPES = ", ".join(IGNORED_FILETYPES)


def remove_ignored_filetypes_scan(files):
    res, nign = split_filetypes_scan(files)

    if nign:
        warn_ignore(nign, "over the whole scan")

    return res


def remove_ignored_filetypes_run(fns):
    res, nign = split_filetypes_run(fns)

    if nign:
        warn_ignore(nign, "for this run")

    return res


def split_filetypes_scan(files):
    scan_nign = 0
    res_files = []
    for fns in files:
        res_fns, run_nign = split_filetypes_run(fns)
        res_files.append(res_fns)
        scan_nign += run_nign

    return res_files, scan_nign


def split_filetypes_run(fns):
    nign = 0
    res_fns = []
    for fn in fns:
        ftype = get_filetype(fn)
        if ftype in IGNORED_FILETYPES:
            nign += 1
        else:
            res_fns.append(fn)

    return res_fns, nign


def warn_ignore(nign, for_what):
    printable_nign = make_printable_nfiles(nign)
    plural_singular = "" if len(IGNORED_FILETYPES) == 1 else "s"
    warn(f"will ignore {printable_nign} {for_what} of the type{plural_singular}: {PRINTABLE_IGNORED_FILETYPES}", stacklevel=3)


def get_filetype(fn):
    return fn.split(".")[-2]

def make_printable_nfiles(n):
    printable = f"{n} file"
    if n != 1:
        printable += "s"
    return printable



