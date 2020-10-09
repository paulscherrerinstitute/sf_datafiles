#!/usr/bin/env python3

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Print statistics for SwissFEL data files")

    parser.add_argument("filenames", type=str, nargs="+", help="names of files to read, accepts wildcards")
    parser.add_argument("-c", "--complete", action="store_true", help="also show channels that have the complete set of pulse IDs")

    clargs = parser.parse_args()


    from sfdata import SFDataFiles

    with SFDataFiles(*clargs.filenames) as data:
        data.print_stats(show_complete=clargs.complete)



if __name__ == '__main__':
    main()



