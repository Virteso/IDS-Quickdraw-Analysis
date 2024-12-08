import numpy as np

import tensorflow as tf
from tensorflow.keras import layers, models
import sklearn.model_selection as msel

import config


def gather_data(class_names=config.DRAWING_NAMES):
    
    print("gathering data.")
    data = []
    labels = []
    for i in range(len(class_names)):
        dname = class_names[i]
        
        print("\t", "loading file", dname + ".npy")
        npa = np.load(config.NUMPY_DRAWING_FOLDER_PATH + config.FILENAME_PREFIX + dname + ".npy")
                
        print("\t\t", "storing...")
        for j in range(min(config.LOAD_DRAWINGS_FROM_EACH_FILE, len(npa))):
            data.append(npa_into_2d_image(npa[j])) # normalise the data too
            labels.append(i)
    
    print("\t", "converting to np...")
    data = np.array(data)
    labels = np.array(labels)
    
    print("split into train and test data.")
    return msel.train_test_split(
        data,
        labels,
        train_size=config.TRAIN_PROPORTION,
        random_state=config.RANDOM_SEED,
    )


def create_model(classes=config.DRAWING_NAMES):
    
    print("creating model.")
    model = models.Sequential()
    model.add(layers.Input(shape=config.DRAWING_IMAGE_SIZE))
    model.add(layers.Conv2D(32, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu", padding="same"))
    
    model.add(layers.Flatten())
    model.add(layers.Dense(65, activation="relu"))
    model.add(layers.Dense(len(classes)))
    
    print("\t", "compiling model...")
    model.compile(optimizer="adam",
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=["accuracy"])
    
    print("\t", "done compiling.")
    return model


def train_model(model, x_train, x_test, y_train, y_test):
    print("training the model...")
    return model.fit(
        x_train,
        y_train,
        epochs=10,
        validation_data=(x_test, y_test)
    )


def npa_into_2d_image(nparr):
	return np.reshape(nparr / 255.0, config.DRAWING_IMAGE_SIZE)
