
class Coordinate():

    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def __repr__(self):
        return f"({self.row}, {self.col})"

class Piece():

    def __init__(self, player='', name=' ', board=None):
        self.player = player
        self.name = name
        self.board = board

    def valid_move(self, start_coord, end_coord):
        """
        Returns True/False for if the user input move is valid given the type of piece.
        Assumes that the move is already valid given dimensions of the board and positions of other pieces.
        """
        return False
    
    def move(self, start_coord, end_coord):
        """
        Executes the move if valid and updates the board.
        Returns a boolean whether the move was successfully executed.
        """
        if not self.valid_move(start_coord, end_coord):
            return False
        self.board[end_coord.row][end_coord.col] = self.board[start_coord.row][start_coord.col]
        self.board[start_coord.row][start_coord.col] = Piece()
        return True
    
class Pawn(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='P', board=board)

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]
        if self.player == 'b':
            if end_piece.player == '':
                if start_row + 1 == end_row and start_col == end_col:
                    return True
                elif start_row + 2 == end_row and start_col == end_col and start_row == 1:
                    return True
            elif end_piece.player == 'w':
                if start_row + 1 == end_row and (start_col - 1 == end_col or start_col + 1 == end_col):
                    return True
        
        elif self.player == 'w':
            if end_piece.player == '':
                if start_row - 1 == end_row and start_col == end_col:
                    return True
                elif start_row - 2 == end_row and start_col == end_col and start_row == 6:
                    return True
            elif end_piece.player == 'b':
                if start_row - 1 == end_row and (start_col - 1 == end_col or start_col + 1 == end_col):
                    return True
        return False
    
    def move(self, start_coord, end_coord):
        """
        Executes the move if valid and updates the board.
        Returns a boolean whether the move was successfully executed.
        """
        if not self.valid_move(start_coord, end_coord):
            return False
        if (end_coord.row == 0 and self.player == 'w') or (end_coord.row == 7 and self.player == 'b'):
            while True:
                raw_input = input("What piece should the pawn become? Please enter 'queen', 'rook', 'knight', or 'bishop'.\n")
                is_valid_format = ["queen", "rook", "knight", "bishop"]
                if raw_input not in is_valid_format:
                    print("Invalid format for move. Please enter 'queen', 'rook', 'knight', or 'bishop'.\n")
                    self.render()
                    continue
                if raw_input == "queen":
                    self.board[end_coord.row][end_coord.col] = Queen(self.player, self.board)
                elif raw_input == "rook":
                    self.board[end_coord.row][end_coord.col] = Rook(self.player, self.board)
                    self.moved = True
                elif raw_input == "knight":
                    self.board[end_coord.row][end_coord.col] = Knight(self.player, self.board)
                elif raw_input == "bishop":
                    self.board[end_coord.row][end_coord.col] = Bishop(self.player, self.board)
                self.board[start_coord.row][start_coord.col] = Piece()
                return True
        self.board[end_coord.row][end_coord.col] = self.board[start_coord.row][start_coord.col]
        self.board[start_coord.row][start_coord.col] = Piece()
        return True
            

class Bishop(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='B', board=board)

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]

        i = start_row
        j = start_col
        if end_col == start_col or end_row == start_row:
            return False
        if end_row < start_row:
            row_dir = -1 
        elif end_row > start_row:
            row_dir = 1
        if end_col < start_col:
            col_dir = -1
        elif end_col > start_col:
            col_dir = 1
        i += row_dir
        j += col_dir
        while i != end_row and j != end_col:
            if self.board[i][j].player != '':
                return False
            i += row_dir
            j += col_dir
        return True

class Knight(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='N', board=board)

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
        return False

class Rook(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='R', board=board)
        self.moved = False

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]
        # row_diff = start_row - end_row
        # col_diff = start_col - end_col
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if row_diff != 0 and col_diff != 0:
            return False
        elif col_diff != 0: # Check right or left
            if col_diff > 0:
                check_range = range(1, col_diff)
            elif col_diff < 0:
                check_range = range(col_diff + 1, 0)
            for i in check_range:
                if self.board[end_row][start_col+i].player != '':
                    return False
            return True 
        elif row_diff != 0: # Check up or down
            if row_diff > 0:
                check_range = range(1, row_diff)
            elif row_diff < 0:
                check_range = range(row_diff + 1, 0)
            for i in check_range:
                print(i)
                if self.board[start_row+i][end_col].player != '':
                    return False
            return True 

    def move(self, start_coord, end_coord):
        """
        Executes the move if valid and updates the board.
        Returns a boolean whether the move was successfully executed.
        """
        if not self.valid_move(start_coord, end_coord):
            return False
        self.board[end_coord.row][end_coord.col] = self.board[start_coord.row][start_coord.col]
        self.board[start_coord.row][start_coord.col] = Piece()
        self.moved = True
        return True

class Queen(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='Q', board=board)

    def valid_move(self, start_coord, end_coord):
        valid_rook = Rook(player=self.player, board=self.board).valid_move(start_coord, end_coord)
        valid_bishop = Bishop(player=self.player, board=self.board).valid_move(start_coord, end_coord)
        return valid_rook or valid_bishop

class King(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='K', board=board)
        self.moved = False

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if row_diff == 1 and col_diff == 1:
            return True
        elif row_diff == 1 and col_diff == 0:
            return True
        elif row_diff == 0 and col_diff == 1:
            return True
        return False
    
    def move(self, start_coord, end_coord):
        """
        Executes the move if valid and updates the board.
        Returns a boolean whether the move was successfully executed.
        """
        if not self.valid_move(start_coord, end_coord):
            return False
        self.board[end_coord.row][end_coord.col] = self.board[start_coord.row][start_coord.col]
        self.board[start_coord.row][start_coord.col] = Piece()
        self.moved = True
        return True