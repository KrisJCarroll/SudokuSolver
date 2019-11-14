from SudokuCell import SudokuCell

class SudokuSolver:
    digits = "123456789" # used for possible values of cells and column numbers
    rows = "ABCDEFGHI" # used to identify each row to generate cells
    cols = digits

    def __init__(self, file):
        cells = [row+col for row in rows for col in cols]
        
        

class Main:
    print("Hello world.")