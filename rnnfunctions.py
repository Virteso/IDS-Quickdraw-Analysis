import tensorflow as tf
from tensorflow.keras import layers, models
import sklearn.model_selection as msel
import numpy as np
import os

import config

# Step 1: Load data with limits
def load_data(output_path="./data/nparrays/", class_names=config.DRAWING_NAMES2, limit_per_class=None, beginning=0):
    """
    Load data from saved numpy arrays and return it with labels.
    Allows limiting the number of samples per class.
    """
    data, labels = [], []
    for idx, name in enumerate(class_names):
        file_path = os.path.join(output_path, f"{name}.npy")
        print(f"Loading data from {file_path}")
        drawings = np.load(file_path)
        if limit_per_class:
            drawings = drawings[beginning:limit_per_class]
        data.append(drawings)
        labels.extend([idx] * len(drawings))
    print("Converting to nparray")
    return np.vstack(data), np.array(labels)

# Step 2: Generate training and testing splits
def split_data(data, labels):
    """
    Split the data into training and testing sets.
    """
    return msel.train_test_split(data, labels, train_size=config.TRAIN_PROPORTION, random_state=config.RANDOM_SEED)

# Step 3: Create the RNN model
def create_rnn_model(input_shape, num_classes):
    """
    Define and compile the RNN model.
    """
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Bidirectional(layers.LSTM(128, return_sequences=True, dropout=0.2)))
    model.add(layers.Bidirectional(layers.LSTM(64, return_sequences=True, dropout=0.2)))
    model.add(layers.Bidirectional(layers.LSTM(64)))

    # Fully connected layers
    model.add(layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
    model.add(layers.Dropout(0.4))
    model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

# Step 4: Train the model with callbacks
def train_model(model, x_train, y_train, x_test, y_test, epochs=config.TRAIN_EPOCHS):
    """
    Train the RNN model with early stopping, learning rate scheduler, and model checkpoint.
    """
    # Early stopping
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=5, restore_best_weights=True
    )

    # Learning rate scheduler
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6
    )

    # Model checkpoint
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath='RNN.keras',
        save_best_only=True,
        monitor='val_loss',
        mode='min'
    )

    return model.fit(
        x_train,
        y_train,
        validation_data=(x_test, y_test),
        epochs=epochs,
        batch_size=32,
        callbacks=[early_stopping, lr_scheduler, model_checkpoint],
    )