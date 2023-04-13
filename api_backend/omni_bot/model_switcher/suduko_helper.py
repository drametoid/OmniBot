import copy
import numpy as np 
import sys
import keras
from detector import detect_sudoku
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

def norm(a):
    return (a/9)-.5

def denorm(a):
    return (a+.5)*9

def inference_sudoku(model, sample):
    '''
        This function solve the sudoku by filling blank positions one by one.
    '''
    feat = copy.copy(sample)
    
    while(1):
        out = model.predict(feat.reshape((1,9,9,1)))  
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((9,9))+1 
        prob = np.around(np.max(out, axis=1).reshape((9,9)), 2) 
        
        feat = denorm(feat).reshape((9,9))
        mask = (feat==0)
     
        if(mask.sum()==0):
            break
            
        prob_new = prob*mask
    
        ind = np.argmax(prob_new)
        x, y = (ind//9), (ind%9)

        val = pred[x][y]
        feat[x][y] = val
        feat = norm(feat)
    return pred

def solve_sudoku_text(model, game):
    game = game.replace('\n', '')
    game = game.replace(' ', '')
    game_arr = np.array([int(j) for j in game]).reshape((9,9,1))
    game_arr = norm(game_arr)
    game_arr_solved = inference_sudoku(model, game_arr)
    return game_arr_solved

def solve_sudoku_img(model, game_arr):
    game_arr = np.array([int(i) for row in game_arr for i in row]).reshape((9,9,1))
    game_arr = norm(game_arr)
    game_arr_solved = inference_sudoku(model, game_arr)
    return game_arr_solved

def solve_suduko(input_type, input_file, saved_model_path=None):
    if saved_model_path is None:
        print(f'ERROR: Model file not found or path not given')
    else:
        model = keras.models.load_model(saved_model_path)
        if input_type == 'img':
            path = os.path.join(script_dir,'detector', 'model', 'cnn.hdf5')
            sudoku_arr = detect_sudoku.get_extracted_digits(path,input_file)
            sudoku_output = solve_sudoku_img(model, sudoku_arr)
            return sudoku_output
        elif input_type == 'txt':
            file = open(input_file, 'r')
            game_input = file.read()
            file.close()
            print(game_input)
            sudoku_output = solve_sudoku_text(model, game_input)
            return sudoku_output
