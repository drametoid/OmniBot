import copy
import keras
import numpy as np
from model import get_model
from preprocess import load_data

import sys

def train_model(x_train, y_train):
    model = get_model()

    adam = keras.optimizers.Adam(lr=.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)

    model.fit(x_train, y_train, batch_size=32, epochs=2)
    return model

def main(input_file, saved_model=None):
    if saved_model is None:
        x_train, x_test, y_train, y_test = load_data(input_file)
        model = train_model(x_train, y_train)
        model.save('model/sudoku.h5')
    else:
        model = keras.models.load_model(saved_model)
    

if __name__ == '__main__':
    input_file = sys.argv[1]
    model = sys.argv[2]
    main(input_file, model)