import ndjson
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import config
import os

def load_and_process_data(file_path, max_seq_len=75):
    print(f"Parsing {file_path}")
    drawings = []
    # Load the ndjson file
    with open(file_path, 'r') as f:
        data = ndjson.load(f)

    for entry in data:
        drawing = entry['drawing']  # List of strokes

        # Convert strokes to a sequence of (x, y) pairs
        strokes = []
        for stroke in drawing:
            x_coords, y_coords = stroke
            strokes.extend(zip(x_coords, y_coords))
            strokes.append((0.0, 0.0))

        # Normalize coordinates (assuming a canvas size of 255x255)
        strokes = [(x / 255.0, y / 255.0) for x, y in strokes]
        drawings.append(strokes)

    # Pad sequences to ensure consistent length
    drawings = pad_sequences(
        drawings,
        maxlen=max_seq_len,
        dtype='float32',
        padding='post',
        value=(0.0, 0.0)  # Use (0,0) for padding
    )

    return np.array(drawings)


def save_data_numpy(array, name="angel"):
    np.save(os.path.join(output, name + ".npy"), array)
    print(f"Data saved to {output}{name}.npy")

def load_data_numpy(name="angel"):
    array = np.load(os.path.join(output, name + ".npy"))
    return array

files = config.DRAWING_NAMES2
data = "./data/json/"
output = "./data/nparrays/"

for name in config.DRAWING_NAMES2:
    save_data_numpy(load_and_process_data(data + name + ".ndjson"), name=name)