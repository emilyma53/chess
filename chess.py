from enum import Enum
import functools
import numpy as np
import pieces
import sys
from termcolor import colored, cprint


class Game:

    def __init__(self):
        """
        Initializes the chessboard as well as the white and black pieces in starting position.
        """
        self.size = 8
        self.board = []
        self.board.append([pieces.Rook('b', self.board), pieces.Knight('b', self.board), pieces.Bishop('b', self.board), pieces.Queen('b', self.board), pieces.King('b', self.board), pieces.Bishop('b', self.board), pieces.Knight('b', self.board), pieces.Rook('b', self.board)])
        self.board.append([pieces.Pawn('b', self.board) for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Piece() for _ in range(self.size)])
        self.board.append([pieces.Pawn('w', self.board) for _ in range(self.size)])
        self.board.append([pieces.Rook('w', self.board), pieces.Knight('w', self.board), pieces.Bishop('w', self.board), pieces.Queen('w', self.board), 
            pieces.King('w', self.board), pieces.Bishop('w', self.board), pieces.Knight('w', self.board), pieces.Rook('w', self.board)])
        
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
                if p.player == '':
                    cprint('   ', 'white', 'on_cyan', end='') if alternate_board == 'cyan' else cprint('   ', 'white', 'on_magenta', end='')
                elif p.player == 'w':
                    cprint(' ' + p.name + ' ', 'white', 'on_cyan', attrs=['bold'], end='') if alternate_board == 'cyan' else cprint(' ' + p.name + ' ', 'white', 'on_magenta', attrs=['bold'], end='')
                elif p.player == 'b':
                    cprint(' ' + p.name + ' ', 'cyan', attrs=['bold', 'reverse'], end='') if alternate_board == 'cyan' else cprint(' ' + p.name + ' ', 'magenta', attrs=['bold', 'reverse'], end='')
                alternate_board = 'magenta' if alternate_board == 'cyan' else 'cyan'
            print('')
        print('\n')

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
            return (pieces.Coordinate(start_row, start_col), pieces.Coordinate(end_row, end_col))

    def play(self):
        self.render()
        print("Begin game of chess. White moves first.")
        curr_player = 'w'
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
            if curr_player == 'w':
                curr_player = 'b'
            else:
                curr_player = 'w'
            self.render()


if __name__ == "__main__":
    game = Game()
    game.play()
