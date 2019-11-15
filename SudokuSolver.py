from SudokuCell import SudokuCell
import csv
import os

class SudokuSolver:
    

    def __init__(self, file):
        self.digits = "123456789" # used for possible values of cells and column numbers
        self.rows = "ABCDEFGHI" # used to identify each row to generate cells
        self.cols = self.digits

        # generate appropriate units
        self.cells = self.cross_product(self.rows, self.cols)
        self.row_units = [self.cross_product(r, self.cols) for r in self.rows]
        self.col_units = [self.cross_product(self.rows, c) for c in self.cols]
        self.row_chunks = ['ABC', 'DEF', 'GHI']
        self.col_chunks = ['123', '456', '789']
        self.square_units = [self.cross_product(r,c) for r in self.row_chunks for c in self.col_chunks]

        # add the units together into a single list of lists
        self.unit_list = self.row_units + self.col_units + self.square_units

        # make a dictionary mapping each cell to their appropriate row, col and square members
        self.cell_units = dict( (cell, [unit for unit in self.unit_list if cell in unit]) for cell in self.cells)

        # make a dictionary mapping each cell to the other cells whose value they must not share
        self.cell_peers = {}
        for cell in self.cells:
            # make a set of all the members of the associated units
            cell_member_list = []
            for unit in self.cell_units[cell]:
                for member in unit:
                    if member != cell and member not in cell_member_list:
                        cell_member_list.append(member)
            self.cell_peers[cell] = cell_member_list

        # testing
        print(self.row_units)
        print()
        print(self.col_units)
        print()
        print(self.square_units)
        print()
        print(self.unit_list)
        print()
        print(self.cell_units['A1'])
        print(self.cell_peers['A1'])

        # get starting values from board state file
        self.start_values = []
        with open(file) as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                for item in line:
                    self.start_values.append(item)

    # helper method for generating cross product lists
    def cross_product(self, A, B):
        return [a+b for a in A for b in B]
        

class Main:
    print("Hello world.")
    path = os.path.dirname(__file__)
    rel_path = 'ExtremeDifficultyTestSudokus/17-1.txt'
    solver = SudokuSolver(os.path.join(path, rel_path))