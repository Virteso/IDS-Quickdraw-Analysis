#!/usr/bin/python3

import numpy as np
import tensorflow as tf
import argparse

import config
import cnnfunctions as fs
import funfunctions as fun


def display_stuff():
    x_train, x_test, y_train, y_test = fs.gather_data()
    for i in range(len(x_test)):
        fun.display_picture(x_test[i])
        if i > 10: break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the file path to the saved numpy drawing file to predict from")
    parser.add_argument("-m", "--modelfile", action="store", help="the file path to the saved keras model, if unspecified we train a new one")
    args = parser.parse_args()
    
    np.random.seed(config.RANDOM_SEED)
    
    model = None
    if args.modelfile:
        print("loading model from file")
        model = tf.keras.models.load_model(args.modelfile)
        print("successfully loaded and compiled")
    else:
        x_train, x_test, y_train, y_test = fs.gather_data()
        model = fs.create_model()
        fs.train_model(model, x_train, x_test, y_train, y_test)
    
    model.summary()
    npa = np.load(args.filename)
    npa = np.reshape(npa / 255.0, (1, config.DRAWING_IMAGE_SIZE, config.DRAWING_IMAGE_SIZE, 1))
    results = fs.get_class_probas(model(npa)[0])
    print("RESULTS:")
    print(results)
    
    
    
    
    
    
