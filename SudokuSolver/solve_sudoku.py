import copy
import numpy as np 
import sys
import keras
from detector import detect_sudoku

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

def main(input_type, input_file, saved_model_path=None):
    if saved_model_path is None:
        print(f'ERROR: Model file not found or path not given')
    else:
        model = keras.models.load_model(saved_model_path)
        if input_type == 'img':
            sudoku_arr = detect_sudoku.get_extracted_digits("detector/model/cnn.hdf5", input_file)
            print(sudoku_arr)
            sudoku_output = solve_sudoku_img(model, sudoku_arr)
            print(f'Solved Sudoku Puzzle is:\n')
            # print(sudoku_output)
            detect_sudoku.display_gameboard(sudoku_output)
            print(f'Verification of solution by summing the digits:')
            verification_sum = np.sum(sudoku_output, axis=1)
            print(verification_sum)
        elif input_type == 'txt':
            file = open(input_file, 'r')
            game_input = file.read()
            file.close()
            print(game_input)
            sudoku_output = solve_sudoku_text(model, game_input)
            print(f'Solved Sudoku Puzzle is:\n')
            # print(sudoku_output)
            detect_sudoku.display_gameboard(sudoku_output)
            print(f'Verification of solution by summing the digits:')
            verification_sum = np.sum(sudoku_output, axis=1)
            print(verification_sum)

if __name__ == '__main__':
    print('''
    Enter the following:\n
    1. input_type= (img|txt) [Either input img or txt depending on kind of input given]\n
    2. Input file path - ex: img.jpg or sudoku.txt\n
    3. Model file path
    ''')
    input_type = sys.argv[1]
    if (input_type not in ['img', 'txt']):
        print('Incorrect input type: {}'.format(input_type))
        sys.exit(1)
    input_file = sys.argv[2]
    model_path = sys.argv[3]
    main(input_type, input_file, model_path)