from enum import Enum
import functools
import pieces
import player
import sys
from termcolor import colored, cprint


class Coordinate():

    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def __repr__(self):
        return f"({self.row}, {self.col})"


class Game:

    def __init__(self):
        """
        Initializes the chessboard as well as the white and black pieces in starting position.
        """
        self.white = player.Player('w')
        self.black = player.Player('b')
        self.size = 8
        self.board = []
        self.board.append([pieces.Rook(self.black, self.board), pieces.Knight(self.black, self.board), pieces.Bishop(self.black, self.board), pieces.Queen(self.black, self.board), pieces.King(self.black, self.board), pieces.Bishop(self.black, self.board), pieces.Knight(self.black, self.board), pieces.Rook(self.black, self.board)])
        self.board.append([pieces.Pawn(self.black, self.board) for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Pawn(self.white, self.board) for _ in range(self.size)])
        self.board.append([pieces.Rook(self.white, self.board), pieces.Knight(self.white, self.board), pieces.Bishop(self.white, self.board), pieces.Queen(self.white, self.board), 
            pieces.King(self.white, self.board), pieces.Bishop(self.white, self.board), pieces.Knight(self.white, self.board), pieces.Rook(self.white, self.board)])
        
    def render(self):
        """
         Prints the board after each turn.
        """
        print('\n')
        print('     a  b  c  d  e  f  g  h')
        print('    ------------------------')
        for index, row in enumerate(self.board):
            label = str(8 - index)
            print(label, '| ', end='')
            if index % 2 == 0:
                alternate_board = 'cyan'
            else:
                alternate_board = 'magenta'
            for p in row:
                if not p.player:
                    cprint('   ', 'white', 'on_cyan', end='') if alternate_board == 'cyan' else cprint('   ', 'white', 'on_magenta', end='')
                elif p.player == self.white:
                    cprint(' ' + p.name + ' ', 'white', 'on_cyan', attrs=['bold'], end='') if alternate_board == 'cyan' else cprint(' ' + p.name + ' ', 'white', 'on_magenta', attrs=['bold'], end='')
                elif p.player == self.black:
                    cprint(' ' + p.name + ' ', 'cyan', attrs=['bold', 'reverse'], end='') if alternate_board == 'cyan' else cprint(' ' + p.name + ' ', 'magenta', attrs=['bold', 'reverse'], end='')
                alternate_board = 'magenta' if alternate_board == 'cyan' else 'cyan'
            print('')
        print("White player's peices: ", end='')
        for piece in self.white.curr_pieces:
            value = self.white.curr_pieces[piece]
            print(piece.name, end=': ')
            print(value, end=' ')
        print("\nBlack player's pieces: ", end='')
        for piece in self.black.curr_pieces:
            value = self.black.curr_pieces[piece]
            print(piece.name, end=': ')
            print(value, end=' ')
        print('\n')
        print('White score:', self.white.get_score())
        print('Black score:', self.black.get_score())

    @staticmethod
    def get_move():
        """
        Processes the user input until a valid move is made. 
        Only checks if the move is within the boundaries and if the move is not stationary.
        Returns (Coordinate(start position), Coordinate(end position))
        """
        column_range = 'abcdefgh'
        row_range = '12345678'
        column_range_msg = "Please enter a column from 'a' to 'h'."
        row_range_msg = "Please enter a row from '1' to '8'."
        while True:
            raw_input = input("Enter player's move. Ex: 'd2 d4' to move a piece from d2 to d4.\n")
            cs = ''.join(raw_input.split()).lower()
            is_valid_format = (len(cs) == 4 and cs[0].isalpha() and cs[1].isdigit() 
                and cs[2].isalpha() and cs[3].isdigit())
            print("cs", cs[0], cs[1], cs[2], cs[3])
            if not is_valid_format:
                print("Invalid format for move. Please enter a move in format 'd2 d4'.\n")
                continue
            elif cs[0] not in column_range or cs[2] not in column_range:
                print("Column not in range. Please enter column in range 'a' to 'h'.")
                continue
            elif cs[1] not in row_range or cs[3] not in row_range:
                print("Row not in range. Please enter row in range '1' to '8'.")
                continue
            elif cs[0] == cs[2] and cs[1] == cs[3]:
                print("Stationary move is not valid. Please pick another move.")
                continue
            start_row = 8 - int(cs[1])
            start_col = ord(cs[0]) - ord('a')
            end_row = 8 - int(cs[3])
            end_col = ord(cs[2]) - ord('a')
            return (Coordinate(start_row, start_col), Coordinate(end_row, end_col))

    def check(self, curr_player):
        '''
        Returns True or False whether the current player is in check 
        (if the chosen move is executed)
        Occurs after calling valid_move
        '''

        return True

    def play(self):
        self.render()
        print("Begin game of chess. White moves first.")
        curr_player = self.white
        while True:
            start_coord, end_coord = Game.get_move()
            start_piece = self.board[start_coord.row][start_coord.col]
            end_piece = self.board[end_coord.row][end_coord.col]
            print("start coord", start_coord.row, start_coord.col)
            print("end coord", end_coord.row, end_coord.col)
            if start_piece.player != curr_player:
                self.render()
                print("Wrong player's turn. Please pick a different move.")
                continue
            if start_piece.player == '':
                self.render()
                print("No piece exists in the starting position. Please pick a different move.")
                continue
            if start_piece.player == end_piece.player:
                self.render()
                print("Player cannot take their own piece. Please pick a different move.")
                continue
            valid_piece_move = self.board[start_coord.row][start_coord.col].move(start_coord, end_coord)
            if not valid_piece_move:
                self.render()
                print("Move not valid given type of piece moving. Please pick a different move.")
                continue
            in_check = self.check(curr_player)
            if curr_player == self.white:
                curr_player = self.black
            else:
                curr_player = self.white
            self.render()


if __name__ == "__main__":
    game = Game()
    game.play()
