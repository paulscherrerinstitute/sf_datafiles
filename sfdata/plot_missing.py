import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


def plot_missing(sfd, show_pids=False, **kwargs):
    data = {}

    sfd.reset_valid()
    pids = sfd.all_pids
    sfd.drop_missing()

    start = min(pids)
    stop = max(pids)
    N = stop - start + 1

    for name, chan in sfd.items():
        bools = indices_to_boolean(chan.valid, N)
        data[name] = bools

    xlabel = "Pulse Indices"
    if show_pids:
        xlabel = "Pulses IDs"
        kwargs.setdefault("start", start)
        kwargs.setdefault("stop", stop)

    kwargs.setdefault("xlabel", xlabel)

    plot_bools(data, **kwargs)


def indices_to_boolean(indices, N):
    res = np.zeros(N, dtype=bool)
    res[indices] = True
    return res


def plot_bools(data, start=0, stop=None, xlabel="Indices", color_true="turquoise", color_false="darkslategrey"):
    cmap = ListedColormap((color_false, color_true))

    if stop is None:
        stop = len(next(iter(data.values())))

    extent = (start, stop, 0, 1)

    ndata = len(data)
    figsize = (10, ndata/2)
    _fig, axes = plt.subplots(ndata, 1, figsize=figsize, sharex=True, squeeze=False)
    axes = axes.ravel()

    for ax, (lbl, arr) in zip(axes, data.items()):
        img = arr[np.newaxis, :]
        ax.imshow(img, aspect="auto", interpolation="nearest", extent=extent, cmap=cmap, vmin=0, vmax=1)
        ax.set_ylabel(lbl, rotation=0, ha="right", va="center")
        ax.set_yticks([])
        ax.tick_params(labelbottom=False)

    ax.tick_params(labelbottom=True)
    ax.set_xlabel(xlabel)

    plt.tight_layout()
    plt.show()





if __name__ == "__main__":
    N = 5000

    data = {
        "A" * 10: np.random.rand(N) > 0.5,
        "B" * 5:  np.random.rand(N) > 0.7,
        "C":      np.random.rand(N) > 0.3,
        "Y":      np.ones([N], dtype=bool),
        "N":      np.zeros([N], dtype=bool)
    }

    plot_bools(data)



