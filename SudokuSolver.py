import sys 
sys.path.append("C:/Users/andre/Documents/School/2019.fall/AI/A4/SudokuSolver/")


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
        # print(self.row_units)
        # print()
        # print(self.col_units)
        # print()
        # print(self.square_units)
        # print()
        # print(self.unit_list)
        # print()
        # print(self.cell_units['A1'])
        # print(self.cell_peers['A1'])

        # get starting values from board state file
        # Map cells to their values per teh file or initialize to a list of all possible values.
        self.cell_values = {}
        counter = 0
        with open(file) as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                for item in line:
                    if int(item) == 0:
                        self.cell_values[self.cells[counter]] = [int(nArr) for nArr in self.digits]
                    else:
                        self.cell_values[self.cells[counter]] = [int(item)]
                    counter += 1

        

        # print(self.cell_values["A1"])
        # print(self.cell_values["A3"])
        
        
        
        # Removes all values which are invalid for each undetermined cell.
        for i, cell in enumerate(self.cells):
            if len(self.cell_values[cell]) == 1:
                for adjCell in self.cell_peers[cell]:
                    if self.cell_values[cell][0] in self.cell_values[adjCell]:
                        self.cell_values[adjCell].remove(self.cell_values[cell][0])
        
        


    # helper method for generating cross product lists
    def cross_product(self, A, B):
        return [a+b for a in A for b in B]
        
        
        
        
    def printBoard(self):
        col = 0
        row = 0
        rowStr = ""
        for i in self.cell_values:
            if len(self.cell_values[i]) > 1:
                rowStr += ". "
            else:
                rowStr += str(self.cell_values[i][0]) + " "
            if (col + 1) % 3 == 0 and col != 0:
                rowStr += "| "
                col = -1
            if (row + 1) % 9 == 0 and row != 0:
                rowStr = rowStr[:-2]
                print(rowStr)
                rowStr = ""
            if (row + 1) % 27 == 0 and row != 0 and row != 80:
                print ("---------------------")
            col += 1
            row += 1
        print (rowStr)
        
    def checkForSingles(self):
        #Check for single values in a block, row, or column here.
        
        

class Main:
    print("Hello world.")
    #path = os.path.dirname(__file__)
    path = "C:/Users/andre/Documents/School/2019.fall/AI/A4/SudokuSolver/"
    rel_path = 'ExtremeDifficultyTestSudokus/17-1.txt'
    solver = SudokuSolver(os.path.join(path, rel_path))
    solver.printBoard()