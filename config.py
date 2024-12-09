NUMPY_DRAWING_FOLDER_PATH = "./data/numpy_bitmap/"
BINARY_DRAWING_FOLDER_PATH = "./data/"
DRAWING_NAMES = [
        "angel", "airplane", "bed", "whale", "shovel",
        "tractor", "panda", "bat", "camel", "cow",
        "ant", "bicycle", "bear", "door", "fan", 
        "flying saucer", "foot", "lipstick","postcard", "popsicle",
        "rainbow", "sock", "strawberry", "washing machine", "yoga"
]
FILENAME_PREFIX = ""

LOAD_DRAWINGS_FROM_EACH_FILE = 1000
TRAIN_PROPORTION = 0.7

DRAWING_IMAGE_SIZE = (
        28, # x
        28, # y
        1, # z (color channel count)
)

RANDOM_SEED = 2343223490

TRAIN_EPOCHS = 10