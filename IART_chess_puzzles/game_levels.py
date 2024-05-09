from strategy import BishopStrategy, KingStrategy, QueenStrategy, KnightStrategy, RookStrategy
from chess_piece import ChessPiece
from position import Position
from board import Board

"""
custom_file format:

<board_size>
<x> <y> <PieceName>
<x> <y> <PieceName>
...
...

"""

pieces_dict = {"Queen": (QueenStrategy(), "Q"),
               "Rook": (RookStrategy(), "R"),
               "Knight": (KnightStrategy(), "k"),
               "King": (KingStrategy(), "K"),
               "Bishop": (BishopStrategy(), "B")}


def generate_board_from_file(filename):
    pieces_placed = {}
    file = open(filename, 'r')
    board_size = int(file.readline())
    board = Board(board_size)
    while True:
        # Get next line from file
        line = file.readline()
        if not line:
            break
        if line == "\n":
            continue
        print("Line: {}".format(line.strip()))
        content = line.split()
        x = int(content[0])
        y = int(content[1])
        piece_name = content[2]
        strategy = pieces_dict[piece_name][0]
        representation = pieces_dict[piece_name][1] + \
            str(pieces_placed.get(piece_name, 0))
        chess_piece = ChessPiece(
            Position(x, y), strategy, representation)
        board.add_piece(chess_piece)
        pieces_placed[piece_name] = pieces_placed.get(piece_name, 0) + 1
        # if line is empty
        # end of file is reached

    board.executePieceMovements()
    board.print()
    return board


def hard_game_board_init():
    BOARD_SIZE = 6
    board = Board(BOARD_SIZE)

    queen_piece = ChessPiece(Position(4, 4), QueenStrategy(), "Q")
    bishop_piece = ChessPiece(Position(1, 4), BishopStrategy(), "B")
    knight_piece = ChessPiece(Position(2, 1), KnightStrategy(), "k")

    board.add_piece(knight_piece)
    board.add_piece(queen_piece)
    board.add_piece(bishop_piece)
    board.executePieceMovements()
    board.print()
    return board


def easy_game_board_init():
    BOARD_SIZE = 5
    board = Board(BOARD_SIZE)

    king_piece = ChessPiece(Position(3, 1), KingStrategy(), "K")
    rook_piece = ChessPiece(Position(1, 1), RookStrategy(), "R")

    board.add_piece(rook_piece)
    board.add_piece(king_piece)
    board.executePieceMovements()
    board.print()
    return board
