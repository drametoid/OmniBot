from detector.image_preprocess import extract as extract_img_grid
from detector.digit_recognition_CNN import run as create_and_save_Model
from detector.predict import extract_number_image as sudoku_extracted

import sys

def display_gameboard(sudoku):
    for i in range(len(sudoku)):
        if i % 3 == 0:
            if i == 0:
                print(" ┎─────────┰─────────┰─────────┒")
            else:
                print(" ┠─────────╂─────────╂─────────┨")

        for j in range(len(sudoku[0])):
            if j % 3 == 0:
                print(" ┃ ", end=" ")

            if j == 8:
                print(sudoku[i][j] if sudoku[i][j] != 0 else ".", " ┃")
            else:
                print(sudoku[i][j] if sudoku[i][j] != 0 else ".", end=" ")

    print(" ┖─────────┸─────────┸─────────┚")

def write_sudoku_to_file(sudoku_arr):
    with open('sudoku.txt', 'w') as file:
        # Iterate over the rows in the array
        for row in sudoku_arr:
            # Write each row to a new line in the file
            file.write(' '.join([str(elem) for elem in row]))
            file.write('\n')

def get_extracted_digits(cnn_model_path, img_path):
    # Calling the image_preprocess.py extract function to get a processed np.array of cells
    image_grid = extract_img_grid(img_path)
    print("Image grid extracted")

    # Sudoku extract
    sudoku = sudoku_extracted(image_grid, cnn_model_path)
    print("Extracted and predicted digits in the Sudoku!")

    print("\n\nInput Sudoku:")
    # write_sudoku_to_file(sudoku)
    display_gameboard(sudoku)
    return sudoku

def main(model_path, img_path):
    # Calling the image_preprocess.py extract function to get a processed np.array of cells
    image_grid = extract_img_grid(img_path)
    print("Image Grid extracted")

    # note we have alreday created and stored the model but if you want to do that again use the following command
    # create_and_save_Model()

    # Sudoku extract
    sudoku = sudoku_extracted(image_grid, model_path)
    print("Extracted and predicted digits in the Sudoku!")

    print("\n\nInput Sudoku:")
    # write_sudoku_to_file(sudoku)
    display_gameboard(sudoku)
    return sudoku

if __name__ == '__main__':
    img_file = sys.argv[1]
    model_path = sys.argv[2]
    main(model_path, img_file)