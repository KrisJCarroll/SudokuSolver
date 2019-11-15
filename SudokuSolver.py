from SudokuCell import SudokuCell
import csv

class SudokuSolver:
    digits = "123456789" # used for possible values of cells and column numbers
    rows = "ABCDEFGHI" # used to identify each row to generate cells
    cols = digits

    def __init__(self, file):
        self.cells = [row+col for row in rows for col in cols]
        with open(file) as f:
            csv_reader = csv.reader(f)
            values = []

        

class Main:
    print("Hello world.")