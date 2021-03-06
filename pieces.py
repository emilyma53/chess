import player
import game

'TODO: Add Checkmate! Add function that lists all valid moves for the given pieces.'
class Piece():

    def __init__(self, player=None, name=' ', board=None):
        self.player = player
        self.name = name
        self.board = board
    
    def all_moves(self, start_coord, end_coord):
        return []

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
        end_piece = self.board[end_coord.row][end_coord.col]
        start_piece = self.board[start_coord.row][start_coord.col]
        if not self.valid_move(start_coord, end_coord):
            return False
        board_copy = self.board.copy()
        self.board[end_coord.row][end_coord.col] = self.board[start_coord.row][start_coord.col]
        self.board[start_coord.row][start_coord.col] = Piece(board=self.board)
        if self.check(self.player, self.get_king_coord()):
            self.board = board_copy
            return False
        if end_piece.player:
            start_piece.player.captured[end_piece] = end_piece.player.curr_pieces[end_piece]
            del end_piece.player.curr_pieces[end_piece]
        return True
    
    def castling(self, start_coord, end_coord):
        return False

    def get_king_coord(self):
        curr_player = self.player
        for i in range(8):
            for j in range(8):
                if not self.board[i][j].player:
                    continue
                if self.board[i][j].player.name == curr_player.name and self.board[i][j].name == 'K':
                    return game.Coordinate(i,j)

    
    def check(self, curr_player, king_coord):
        '''
        Returns True or False whether the current player is in check 
        (if the chosen move is executed)
        Occurs after calling valid_move
        '''
        if not curr_player:
            print("CURR PLAYER IS NONE")
        if curr_player.name == 'w':
            opp_player_name = 'b'
        else:
            opp_player_name = 'w'
        for i in range(8):
            for j in range(8):
                if not self.board[i][j].player:
                    continue
                if self.board[i][j].player.name == opp_player_name:
                    if self.board[i][j].valid_move(game.Coordinate(i,j), king_coord):
                        print(self.board[i][j].name, self.board[i][j].player.name, i, j)
                        print(king_coord.row, king_coord.col)
                        return True        
        return False
    
class Pawn(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='P', board=board)
        self.player.curr_pieces[self] = 1

    def all_moves(self, start_coord):
        all_moves = []
        start_row = start_coord.row
        start_col = start_coord.col
        if self.player.name == 'b':
            if not self.board[start_row + 1][start_col].player:
                all_moves.append(game.Coordinate(start_row + 1, start_col))
            if not self.board[start_row + 2][start_col].player and start_row == 1:
                if not self.board[start_row + 1][start_col].player:
                    all_moves.append(game.Coordinate(start_row + 2, start_col))
            if self.board[start_row + 1][start_col - 1].player.name == 'w':
                all_moves.append(game.Coordinate(start_row + 1, start_col - 1))
            if self.board[start_row + 1][start_col + 1].player.name == 'w':
                all_moves.append(game.Coordinate(start_row + 1, start_col + 1))
        elif self.player.name == 'w':
            if not self.board[start_row - 1][start_col].player:
                all_moves.append(game.Coordinate(start_row - 1, start_col))
            if not self.board[start_row - 2][start_col].player and start_row == 6:
                if not self.board[start_row - 1][start_col].player:
                    all_moves.append(game.Coordinate(start_row - 2, start_col))
            if self.board[start_row - 1][start_col - 1].player.name == 'b':
                all_moves.append(game.Coordinate(start_row - 1, start_col - 1))
            if self.board[start_row - 1][start_col + 1].player.name == 'b':
                all_moves.append(game.Coordinate(start_row - 1, start_col + 1))
        return all_moves
            

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]
        if end_piece.player == self.board[start_row][start_col].player:
            return False
        if self.player.name == 'b':
            if not end_piece.player:
                if start_row + 1 == end_row and start_col == end_col:
                    return True
                elif start_row + 2 == end_row and start_col == end_col and start_row == 1:
                    if not self.board[start_row+1][start_col].player:
                        return True
            elif end_piece.player.name == 'w':
                if start_row + 1 == end_row and (start_col - 1 == end_col or start_col + 1 == end_col):
                    return True
        
        elif self.player.name == 'w':
            if not end_piece.player:
                if start_row - 1 == end_row and start_col == end_col:
                    return True
                elif start_row - 2 == end_row and start_col == end_col and start_row == 6:
                    if not self.board[start_row-1][start_col].player:
                        return True
            elif end_piece.player.name == 'b':
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
        end_piece = self.board[end_coord.row][end_coord.col]
        start_piece = self.board[start_coord.row][start_coord.col]
        board_copy = self.board.copy()
        self.board[end_coord.row][end_coord.col] = self.board[start_coord.row][start_coord.col]
        self.board[start_coord.row][start_coord.col] = Piece(board=self.board)
        if self.check(self.player, self.get_king_coord()):
            self.board = board_copy
            return False
        if (end_coord.row == 0 and self.player.name == 'w') or (end_coord.row == 7 and self.player.name == 'b'):
            self.board = board_copy
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
                if end_piece.player:
                    start_piece.player.captured[end_piece] = end_piece.player.curr_pieces[end_piece]
                    del end_piece.player.curr_pieces[end_piece]
                del start_piece.player.curr_pieces[start_piece]
                self.board[start_coord.row][start_coord.col] = Piece(board=self.board)
                return True
        if end_piece.player:
            start_piece.player.captured[end_piece] = end_piece.player.curr_pieces[end_piece]
            del end_piece.player.curr_pieces[end_piece]
        return True
            

class Bishop(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='B', board=board)
        self.player.curr_pieces[self] = 3

    def all_moves(self, start_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        all_moves = []
        directions = [(1,1), (-1,1), (1,-1), (-1, -1)]
        for row_dir, col_dir in directions:
            i = start_row + row_dir
            j = start_col + col_dir
            while not self.board[i][j].player:
                if self.board[i][j].player or i < 0 or j < 0 or i > 7 or j > 7:
                    break
                all_moves.append(game.Coordinate(i,j))
                i += row_dir
                j += col_dir
            if self.board[i][j].player:
                if self.board[i][j].player != self.player:
                    all_moves.append(game.Coordinate(i,j))
        return all_moves


    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]

        if end_piece.player == self.board[start_row][start_col].player:
            return False

        i = start_row
        j = start_col
        if end_col == start_col or end_row == start_row:
            return False
        if abs(end_col - start_col) != abs(end_row - start_row):
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
            if self.board[i][j].player or i < 0 or j < 0 or i > 7 or j > 7:
                return False
            i += row_dir
            j += col_dir
        return True

class Knight(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='N', board=board)
        self.player.curr_pieces[self] = 3

    def all_moves(self, start_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        all_moves = []
        all_moves.append(game.Coordinate(start_row+1, start_col+2))
        all_moves.append(game.Coordinate(start_row+1, start_col+1))
        all_moves.append(game.Coordinate(start_row-1, start_col+2))
        all_moves.append(game.Coordinate(start_row-1, start_col+1))
        all_moves.append(game.Coordinate(start_row+2, start_col+2))
        all_moves.append(game.Coordinate(start_row+2, start_col+1))
        all_moves.append(game.Coordinate(start_row-2, start_col+2))
        all_moves.append(game.Coordinate(start_row-2, start_col+1))
        for move in all_moves:
            if move.row < 0 or move.row > 7 or move.col < 0 or move.col > 7:
                all_moves.remove(move)
            elif self.board[move.row][move.col].player == self.player:
                all_moves.remove(move)
        return all_moves

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        if end_piece.player == self.board[start_row][start_col].player:
            return False

        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
        return False

class Rook(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='R', board=board)
        self.moved = False
        self.player.curr_pieces[self] = 5
    
    def all_moves(self, start_coord):
        # does not include possible castling
        start_row = start_coord.row
        start_col = start_coord.col
        all_moves = []
        directions = [(1,0), (-1,0), (0,-1), (0, 1)]
        for row_dir, col_dir in directions:
            i = start_row + row_dir
            j = start_col + col_dir
            while not self.board[i][j].player:
                if self.board[i][j].player or i < 0 or j < 0 or i > 7 or j > 7:
                    break
                all_moves.append(game.Coordinate(i,j))
                i += row_dir
                j += col_dir
            if self.board[i][j].player:
                if self.board[i][j].player != self.player:
                    all_moves.append(game.Coordinate(i,j))
        return all_moves

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        end_piece = self.board[end_row][end_col]
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if end_piece.player == self.board[start_row][start_col].player:
            return False

        if row_diff != 0 and col_diff != 0:
            return False
        elif col_diff != 0: # Check right or left
            if col_diff > 0:
                check_range = range(1, col_diff)
            elif col_diff < 0:
                check_range = range(col_diff + 1, 0)
            for i in check_range:
                if self.board[end_row][start_col+i].player:
                    return False
            return True 
        elif row_diff != 0: # Check up or down
            if row_diff > 0:
                check_range = range(1, row_diff)
            elif row_diff < 0:
                check_range = range(row_diff + 1, 0)
            for i in check_range:
                print(i)
                if self.board[start_row+i][end_col].player:
                    return False
            return True 

    def move(self, start_coord, end_coord):
        """
        Executes the move if valid and updates the board.
        Returns a boolean whether the move was successfully executed.
        """
        valid_move = Piece.move(self, start_coord, end_coord)
        if not valid_move:
            return False
        self.moved = True
        return True

class Queen(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='Q', board=board)
        self.player.curr_pieces[self] = 9
    
    def all_moves(self, start_coord):
        rook = Rook(player=self.player, board=self.board)
        rook_moves = rook.all_moves(start_coord)
        bishop = Bishop(player=self.player, board=self.board)
        bishop_moves = bishop.all_moves(start_coord)
        del self.player.curr_pieces[rook]
        del self.player.curr_pieces[bishop]
        return rook_moves + bishop_moves

    def valid_move(self, start_coord, end_coord):
        rook = Rook(player=self.player, board=self.board)
        bishop = Bishop(player=self.player, board=self.board)
        valid_rook = rook.valid_move(start_coord, end_coord)
        valid_bishop = bishop.valid_move(start_coord, end_coord)
        del self.player.curr_pieces[rook]
        del self.player.curr_pieces[bishop]
        return valid_rook or valid_bishop

class King(Piece):

    def __init__(self, player, board):
        Piece.__init__(self, player=player, name='K', board=board)
        self.moved = False
        self.player.curr_pieces[self] = 0
    
    def all_moves(self, start_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        all_moves = []
        for row in range(start_row - 1, start_row + 2):
            for col in range(start_col - 1, start_col + 2):
                if row < 0 or row > 7 or col < 0 or col > 7:
                    continue
                elif row == start_row and col == start_col:
                    continue
                elif self.board[row][col].player:
                    if self.board[row][col].player != self.player:
                        all_moves.append(game.Coordinate(row, col))
        return all_moves

    def valid_move(self, start_coord, end_coord):
        start_row = start_coord.row
        start_col = start_coord.col
        end_row = end_coord.row
        end_col = end_coord.col
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if self.board[end_row][end_col].player == self.board[start_row][start_col].player:
            return False
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
        valid_move = Piece.move(self, start_coord, end_coord)
        if not valid_move:
            return False
        self.moved = True
        return True

    def castling(self, start_coord, end_coord):
        """
        Returns True or False if castling is valid. 
        Start_coord must be player's king and end_coord must be a rook.
        Both rook and king must have never been moved before.
        The king, rook, or any square in between cannot be currently attacked.
        """
        if self.board[end_coord.row][end_coord.col].name != 'R':
            return False
        if self.board[end_coord.row][end_coord.col].moved or self.moved:
            return False
        col_diff = end_coord.col - start_coord.col
        if col_diff < 0:
            col_range1 = range(2, 5)
            col_range2 = range(1, 4)
        elif col_diff > 0:
            col_range1 = range(4, 7)
            col_range2 = range(5, 8)
        for i in col_range1:
            if self.check(self.player, game.Coordinate(start_coord.row, i)):
                return False
        for i in col_range2:
            if self.board[start_coord.row][i].player:
                return False
        self.moved = True
        if end_coord.col == 7:
            self.board[start_coord.row][5] = self.board[start_coord.row][7]
            self.board[start_coord.row][7] = Piece(board=self.board)
            self.board[start_coord.row][6] = self.board[start_coord.row][4]
            self.board[start_coord.row][4] = Piece(board=self.board)
        elif end_coord.col == 0:
            self.board[start_coord.row][3] = self.board[start_coord.row][0]
            self.board[start_coord.row][0] = Piece(board=self.board)
            self.board[start_coord.row][2] = self.board[start_coord.row][4]
            self.board[start_coord.row][4] = Piece(board=self.board)
        else:
            print("ERROR WITH CASTLING CODE")
        return True
        


