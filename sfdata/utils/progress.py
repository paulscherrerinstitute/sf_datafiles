import numpy as np


def bar(perc, block="▇", n_blocks_total=10):
    n = _n_blocks(perc, n_blocks_total)
    return block * n

def dip(perc, block="▇", n_blocks_total=10):
    n = _n_blocks(perc, n_blocks_total)
    n = n_blocks_total - n
    return block * n

def _n_blocks(perc, n_blocks_total):
    divider = 100 / n_blocks_total
    return int(np.ceil(perc / divider))


def percentage(n, ntotal, decimals=0):
    ratio = n / ntotal
    return _percentage(ratio, decimals)

def percentage_missing(n, ntotal, decimals=0):
    ratio = n / ntotal
    ratio = 1 - ratio
    return _percentage(ratio, decimals)

def _percentage(ratio, decimals):
    ratio *= 100
    ratio = round(ratio, decimals)
    if decimals == 0:
        return int(ratio)
    return ratio


def decide_color(n, nmin, nmax): #TODO: more level? decide upon percentages?
    if n == nmax:
        return "green"
    elif n == nmin:
        return "red"
    else:
        return None



