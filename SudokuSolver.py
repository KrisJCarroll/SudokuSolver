import sys 
sys.path.append("C:/Users/andre/Documents/School/2019.fall/AI/A4_4/SudokuSolver/")


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

    # helper method for generating cross product lists
    def cross_product(self, A, B):
        return [a+b for a in A for b in B]

    # checking to see if board is solved (all cells have a single value)
    def solved(self):
        for cell in self.cells:
            if len(self.cell_values[cell]) > 1:
                return False 
        return True
    
    # checking to see if board is unsolvable (any cell has 0 possible remaining values)
    def is_invalid(self):
        if len([cell for cell, values in self.cell_values if len(values) == 0]):
            return True
        return False
        
    def printBoard(self):
        col = 0
        row = 0
        rowStr = ""
        for i in self.cell_values:
            if len(self.cell_values[i]) > 1:
                rowStr += ". "
            elif len(self.cell_values[i]) < 1:
                print(i, "LESS THAN 1")
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
        print("---------------------------------")
    

    def removeInvalid(self):
        removed = False
        # Removes all values which are invalid for each undetermined cell.
        for i, cell in enumerate(self.cells):
            if len(self.cell_values[cell]) == 1:
                for adjCell in self.cell_peers[cell]:
                    if self.cell_values[cell][0] in self.cell_values[adjCell] and len(self.cell_values[adjCell]) > 1:
                        self.cell_values[adjCell].remove(self.cell_values[cell][0])
                        if len(self.cell_values[adjCell]) == 0:
                            print("{c1} was just emptied to 0 due to {c2}'s value of {value}".format(c1=adjCell, c2=cell, value=self.cell_values[cell][0]))
                        removed = True
        return removed
                        
                        
    def removeInvalidCell(self, cell):
        # Removes all values which are invalid for each undetermined cell
        for adjCell in self.cell_peers[cell]:
            if self.cell_values[cell][0] in self.cell_values[adjCell] and len(self.cell_values[adjCell]) > 1:
                self.cell_values[adjCell].remove(self.cell_values[cell][0])
                        
    
    def checkForSingles(self, units):
        found = False
        for unit in units:
            tmpLst = [0,0,0,0,0,0,0,0,0]
            for cell in unit:
                if len(self.cell_values[cell]) > 1:
                    for val in self.cell_values[cell]:
                        tmpLst[val - 1] += 1
            if 1 in tmpLst:
                singleNum = tmpLst.index(1) + 1
                for cell in unit:
                    if singleNum in self.cell_values[cell]: #FOUND
                        print("FOUND")
                        self.cell_values[cell] = [singleNum]
                        self.removeInvalidCell(cell)
                        tmpLst[tmpLst.index(1)] = 0
                        return True 
                        found = True
        return found


    #Check for single values in a block, row, or column here.
    def run_constraints(self):
        stuck = False
        
        # constraint propagation goes here
        while not stuck:
            tests = [True, True] # initialize to True for each test run
            tests[0] = self.removeInvalid()
            #tests[1] = self.checkForSingles(self.unit_list)
            tests[1] = self.trimPotentialValues(self.unit_list)
            
            # nothing changed on the iteration, we're stuck
            if True not in tests:
                stuck = True 

            # if any of the cells have no possible options remaining, we have an invalid board
            if self.is_invalid():
                return False
        
        return True
        
    
    def solve(self):
        # running constraints didn't produce an invalid board state
        if(self.run_constraints()):
            # check for solved status and if not solved, we need to start trying options
            if not self.solved():
                self.printBoard()
                print("We need to do more.")

            # we beat the game, print it and brag a lot
            else:
                self.printBoard()
                print("Solved! So strong.")
        # the initial state produced an invalid puzzle after applying constraints - the puzzle cannot be solved
        else:
            print("This puzzle is unsolvable.")
            return False
        
    def trimPotentialValues(self, unitType): #Checks in all units for specific numbers, then removes all instances of those numbers in their shared units.

        totTrimmed = 0
        trimmedVals = False
        tList = [0,0,0,0,0,0,0,0,0]
        
        for unit in unitType:
            tList = [0,0,0,0,0,0,0,0,0]
            for cell in unit:
                if len(self.cell_values[cell]) > 1:
                    for val in self.cell_values[cell]:
                        tList[val - 1] += 1
                    
            for ndx, val in enumerate(tList):
                if val == 1: #SINGLE VALUE - replacing "find single values"
                    singleNum = ndx + 1
                    for cell in unit:
                        for findVall in self.cell_values[cell]:
                            if findVall == singleNum: #congratulations you found the single number.
                                self.cell_values[cell] = [singleNum]
                                self.removeInvalidCell(cell)
                                return True
                                trimmedVals = True
    
                elif val > 1:
                    singleNum = ndx + 1 #now find the amount of cells with the same vals
                    uCellList = []
                    for cell in unit:
                        for findVall in self.cell_values[cell]:
                            if findVall == singleNum:
                                uCellList.append(cell)
                    for findUnit in self.unit_list:
                        if set(uCellList).issubset(findUnit):
                            for modCell in findUnit:
                                if modCell not in uCellList and singleNum in self.cell_values[modCell]:
                                    self.cell_values[modCell].remove(singleNum)
                                    return True
                                    trimmedVals = True
                                    totTrimmed += 1
                                    

                                
                    
        print (totTrimmed)
        return trimmedVals
        
    # def checkForSingles(self, units):
    #     found = False
    #     for unit in units:
    #         tmpLst = [0,0,0,0,0,0,0,0,0]
    #         for cell in unit:
    #             if len(self.cell_values[cell]) > 1:
    #                 for val in self.cell_values[cell]:
    #                     tmpLst[val - 1] += 1
    #         if 1 in tmpLst:
    #             singleNum = tmpLst.index(1) + 1
    #             for cell in unit:
    #                 if singleNum in self.cell_values[cell]: #FOUND
    #                     print("FOUND")
    #                     self.cell_values[cell] = [singleNum]
    #                     self.removeInvalidCell(cell)
    #                     tmpLst[tmpLst.index(1)] = 0
    #                     found = True
    #     return found

class Main:
    print("Hello world.")
    #path = os.path.dirname(__file__)
    path = "C:/Users/andre/Documents/School/2019.fall/AI/A4_4/SudokuSolver/"
    rel_path = 'ExtremeDifficultyTestSudokus/17-1.txt'
    solver = SudokuSolver(os.path.join(path, rel_path))
    solver.printBoard()
    solver.solve()
    easy_path = 'EasyDifficultyTestSudokus/easy-1.txt'
    solver = SudokuSolver(os.path.join(path, easy_path))
    solver.solve()
    #solver.checkForSingles(solver.row_units)
    #solver.checkForSingles(solver.col_units)
    solver.printBoard()
