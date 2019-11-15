from SudokuCell import SudokuCell
import csv
import os

class SudokuSolver:
    

    def __init__(self, file):
        digits = "123456789" # used for possible values of cells and column numbers
        rows = "ABCDEFGHI" # used to identify each row to generate cells
        cols = digits

        self.cells = self.cross_product(rows, cols)
        self.row_units = [self.cross_product(r, cols) for r in rows]
        self.col_units = [self.cross_product(rows, c) for c in cols]
        row_chunks = ['ABC', 'DEF', 'GHI']
        col_chunks = ['123', '456', '789']
        self.square_units = [self.cross_product(r,c) for r in row_chunks for c in col_chunks]
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