from time import sleep
from chess_piece import ChessPiece
from position import Position
from itertools import combinations


class Solver:
    def __init__(self, initial_pos, final_pos, board_size, board, chess_pieces) -> None:
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        self.board_size = board_size
        self.matrix = board
        self.chess_pieces = chess_pieces

    def solve(self):
        pass
