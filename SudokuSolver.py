from SudokuCell import SudokuCell
import csv
import os

class SudokuSolver:
    digits = "123456789" # used for possible values of cells and column numbers
    rows = "ABCDEFGHI" # used to identify each row to generate cells
    cols = digits

    def __init__(self, file):
        self.cells = [row+col for row in SudokuSolver.rows for col in SudokuSolver.cols]
        self.start_values = []
        with open(file) as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                for item in line:
                    self.start_values.append(item)
            

        

class Main:
    print("Hello world.")
    path = os.path.dirname(__file__)
    rel_path = 'ExtremeDifficultyTestSudokus/17-1.txt'
    solver = SudokuSolver(os.path.join(path, rel_path))