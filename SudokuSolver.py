from SudokuCell import SudokuCell
import csv
import os

class SudokuSolver:
    

    def __init__(self, file):
        self.digits = "123456789" # used for possible values of cells and column numbers
        self.rows = "ABCDEFGHI" # used to identify each row to generate cells
        self.cols = self.digits

        self.cells = self.cross_product(self.rows, self.cols)
        self.row_units = [self.cross_product(r, self.cols) for r in self.rows]
        self.col_units = [self.cross_product(self.rows, c) for c in self.cols]
        self.row_chunks = ['ABC', 'DEF', 'GHI']
        self.col_chunks = ['123', '456', '789']
        self.square_units = [self.cross_product(r,c) for r in self.row_chunks for c in self.col_chunks]
        print(self.row_units)
        print()
        print(self.col_units)
        print()
        print(self.square_units)
        self.start_values = []
        with open(file) as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                for item in line:
                    self.start_values.append(item)

    def cross_product(self, A, B):
        return [a+b for a in A for b in B]
        

class Main:
    print("Hello world.")
    path = os.path.dirname(__file__)
    rel_path = 'ExtremeDifficultyTestSudokus/17-1.txt'
    solver = SudokuSolver(os.path.join(path, rel_path))