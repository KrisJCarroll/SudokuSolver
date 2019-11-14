class SudokuCell:

    def __init__(self, identifier, value, row_membs, col_membs, square_membs):
        self.identifier = identifier
        self.value = value
        self.row_membs = row_membs
        self.col_membs = col_membs
        self.square_membs = square_membs

