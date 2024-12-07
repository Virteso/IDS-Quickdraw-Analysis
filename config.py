DRAWING_FOLDER_PATH = "./data/numpy_bitmap/"
DRAWING_NAMES = [
        "airplane", "bed", "whale", "shovel",
        "tractor", "panda", "bat", "camel",
        "cow", "ant", "smiley face",
]

LOAD_DRAWINGS_FROM_EACH_FILE = 2000
TRAIN_PROPORTION = 0.7

DRAWING_IMAGE_SIZE = (
        28, # x
        28, # y
        1, # z (color channel count)
)

RANDOM_SEED = 11