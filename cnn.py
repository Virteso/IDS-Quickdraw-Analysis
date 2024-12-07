import numpy as np

import config
import cnnfunctions as fs
import funfunctions as fun


def display_stuff():
    x_train, x_test, y_train, y_test = fs.gather_data()
    for i in range(len(x_test)):
        fun.display_picture(x_test[i])
        if i > 10: break


if __name__ == "__main__":
    np.random.seed(config.RANDOM_SEED)
    x_train, x_test, y_train, y_test = fs.gather_data()
    fun.display_picture(x_train[0])
    model = fs.create_model()
    model.summary()
    history = fs.train_model(model, x_train, x_test, y_train, y_test)
    
    
    
