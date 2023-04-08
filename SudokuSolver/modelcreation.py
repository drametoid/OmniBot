import keras
import numpy as np
from model import get_model
from preprocess import load_data
from solve_sudoku import inference_sudoku

import sys

def train_model(x_train, y_train):
    model = get_model()

    adam = keras.optimizers.Adam(lr=.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)

    model.fit(x_train, y_train, batch_size=32, epochs=2)
    return model

def test_accuracy(feats, labels):
    
    correct = 0
    
    for i,feat in enumerate(feats):
        pred = inference_sudoku(feat)
        true = labels[i].reshape((9,9))+1
        if(abs(true - pred).sum()==0):
            correct += 1
    print(f'Accuracy is {correct/feats.shape[0]}')

def main(input_file, saved_model=None, get_test_accuracy=False):
    x_train, x_test, y_train, y_test = load_data(input_file)
    if saved_model is None:
        model = train_model(x_train, y_train)
        model.save('model/sudoku.h5')
    else:
        model = keras.models.load_model(saved_model)

    if(get_test_accuracy):
        test_accuracy(x_test[:100], y_test[:100])
    

if __name__ == '__main__':
    input_file = sys.argv[1]
    model = sys.argv[2]
    get_test_accuracy = bool(sys.argv[3])
    main(input_file, model, get_test_accuracy)