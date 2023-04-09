import keras
import numpy as np
from model import get_model
from preprocess_data import load_data
from solve_sudoku import inference_sudoku

import sys
import os

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

def main(input_file, saved_model_path=None, get_test_accuracy=False):
    x_train, x_test, y_train, y_test = load_data(input_file)
    if saved_model_path is (None or '.'):
        print(f'Training and saving model now...')
        model = train_model(x_train, y_train)
        model.save('model/sudoku.h5')
    else:
        if os.path.isfile(saved_model_path):
            try:
                print(f'Found saved model. Loading now..')
                model = keras.models.load_model(saved_model_path)
                print(f'Model loaded!')
            except Exception as e:
                print(f'Error encountered: {e}')
                sys.exit(1)
        else:
            print('ERROR: Unable to load model or wrong path provided!')
            sys.exit(1)
    

if __name__ == '__main__':
    print(f'''Following input arguments need to be provided:\n
    1. csv file for model training
    2. Model file path (if exists). If re-training or doesn't exist give '.' as input (without the ')
    3. getAccuracyData flag: 1 or 0 as boolean input (100 puzzles are tested to get accuracy of the model)
    '''
        )
    input_file = sys.argv[1]
    model_path = sys.argv[2]
    get_test_accuracy = bool(sys.argv[3])
    print(f'Input file provided: {input_file}')
    print(f'Model file provided: {model_path}')
    print(f'Accuracy requested: {get_test_accuracy}')
    main(input_file, model_path, get_test_accuracy)