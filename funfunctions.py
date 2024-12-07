import numpy as np
import matplotlib.pyplot as plt


def display_picture(ndarr):
    if len(ndarr.shape) != 2:
        ndarr = np.reshape(ndarr, ndarr.shape[:-1])
    plt.imshow(ndarr, cmap="gray", vmin=0.0, vmax=1.0)
    plt.show()