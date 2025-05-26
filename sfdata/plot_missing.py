import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


def plot_missing(sfd, **kwargs):
    data = {}

    sfd.reset_valid()
    pids = sfd.all_pids
    N = max(pids) - min(pids) + 1
    sfd.drop_missing()

    for name, chan in sfd.items():
        bools = indices_to_boolean(chan.valid, N)
        data[name] = bools

    plot_bools(data, **kwargs)


def indices_to_boolean(indices, N):
    res = np.zeros(N, dtype=bool)
    res[indices] = True
    return res


def plot_bools(data, color_true="turquoise", color_false="darkslategrey"):
    cmap = ListedColormap((color_false, color_true))

    ndata = len(data)
    length = len(next(iter(data.values())))
    extent = (0, length, 0, 1) #TODO: pulse IDs?

    fig, axes = plt.subplots(ndata, 1, figsize=(10, ndata/2), sharex=True, squeeze=False)
    axes = axes.ravel()

    for i, (ax, (lbl, arr)) in enumerate(zip(axes, data.items())):
        img = arr[np.newaxis, :]
        ax.imshow(img, aspect="auto", interpolation="nearest", extent=extent, cmap=cmap, vmin=0, vmax=1)
        ax.set_ylabel(lbl, rotation=0, ha="right", va="center")
        ax.set_yticks([])
        ax.tick_params(labelbottom=False)

    ax.tick_params(labelbottom=True)
    ax.set_xlabel("Pulses")

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



