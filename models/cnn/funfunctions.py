import numpy as np
import matplotlib.pyplot as plt
import subprocess

import config


def display_picture(ndarr):
    if len(ndarr.shape) != 2:
        ndarr = np.reshape(ndarr, ndarr.shape[:-1])
    plt.imshow(ndarr, cmap="gray", vmin=0.0, vmax=1.0)
    plt.show()


def large_files():
    for drawingname in config.DRAWING_NAMES:
        filename = config.BINARY_DRAWING_FOLDER_PATH + drawingname + ".bin"
        print("converting ", filename)
        output = config.NUMPY_DRAWING_FOLDER_PATH + "HUGE" + drawingname + ".npy"
        ob = subprocess.run(["./readqd",
                        "--file", filename,
                        "-n", str(config.LOAD_DRAWINGS_FROM_EACH_FILE),
                        "--output", output])
        print("saved to", output)
        print(ob.check_returncode())